from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pos_boilerplate.cli import main
from pos_boilerplate.secrets import (
    MAX_SCANNED_BYTES,
    _read_bounded_file,
    redact_path,
    scan_repository,
    scan_text,
)


class SecretScanTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(
            ["git", "-C", str(root), "config", "user.email", "test@example.com"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(root), "config", "user.name", "Test"],
            check=True,
        )

    def commit_all(self, root: Path, message: str) -> None:
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", message], check=True)

    def test_scan_text_detects_token_without_returning_its_value(self) -> None:
        credential_value = "gh" + "p_" + "A" * 36

        findings = scan_text(f"credential = {credential_value}\n", "config.txt")

        self.assertEqual({finding.rule_id for finding in findings}, {"GITHUB_TOKEN"})
        rendered = "\n".join(finding.render() for finding in findings)
        self.assertNotIn(credential_value, rendered)
        self.assertIn("config.txt:1", rendered)

    def test_scan_text_allows_placeholders_and_environment_references(self) -> None:
        text = "\n".join(
            (
                'api_key = "your_api_key"',
                'auth_token = os.environ.get("AUTH_TOKEN")',
                'password = ${PASSWORD}',
                'client_secret = "<from-password-manager>"',
            )
        )

        self.assertEqual(scan_text(text, "example.env"), ())

    def test_placeholder_word_inside_real_credential_does_not_bypass_scan(self) -> None:
        findings = scan_text(
            "pass" + "word=prod-" + "example-credential\n",
            "config.env",
        )

        self.assertEqual(
            {finding.rule_id for finding in findings},
            {"GENERIC_CREDENTIAL_ASSIGNMENT"},
        )

    def test_scan_text_checks_every_assignment_on_a_line(self) -> None:
        findings = scan_text(
            "to" + "ken=your_token pass" + "word=actual-production-password\n",
            "config.env",
        )

        self.assertEqual(
            {finding.rule_id for finding in findings},
            {"GENERIC_CREDENTIAL_ASSIGNMENT"},
        )

    def test_history_scan_finds_a_removed_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "README.md").write_text("clean\n", encoding="utf-8")
            self.commit_all(root, "initial")
            credential_value = "sk-" + "A" * 24
            (root / "removed.env").write_text(
                f"{'to' + 'ken'}={credential_value}\n", encoding="utf-8"
            )
            self.commit_all(root, "add credential")
            (root / "removed.env").unlink()
            self.commit_all(root, "remove credential")

            current = scan_repository(root, include_history=False)
            history = scan_repository(root, include_history=True)

            self.assertTrue(current.ok)
            self.assertFalse(history.ok)
            self.assertIn("OPENAI_STYLE_TOKEN", {item.rule_id for item in history.findings})
            self.assertNotIn(
                credential_value,
                "\n".join(item.render() for item in history.findings),
            )

    def test_history_scan_checks_commit_messages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "README.md").write_text("clean\n", encoding="utf-8")
            credential_value = "sk-" + "B" * 24
            self.commit_all(
                root,
                f"remove {'to' + 'ken'}={credential_value}",
            )

            result = scan_repository(root, include_history=True)

            self.assertFalse(result.ok)
            rendered = "\n".join(item.render() for item in result.findings)
            self.assertIn("OPENAI_STYLE_TOKEN", rendered)
            self.assertNotIn(credential_value, rendered)

    def test_private_markers_respect_the_public_safe_list(self) -> None:
        findings = scan_text(
            "Hermes\nPrivate Person\n",
            "example.md",
            private_markers=("Hermes", "Private Person"),
            public_safe_terms=("Hermes",),
        )

        self.assertEqual(1, len(findings))
        self.assertTrue(findings[0].rule_id.startswith("PRIVATE_MARKER_"))

    def test_history_scan_detects_and_redacts_sensitive_removed_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            private_marker = "Private Person"
            sensitive_path = root / f"{private_marker}.md"
            sensitive_path.write_text("clean content\n", encoding="utf-8")
            self.commit_all(root, "add path fixture")
            sensitive_path.unlink()
            self.commit_all(root, "remove path fixture")

            result = scan_repository(
                root,
                include_history=True,
                private_markers=(private_marker,),
            )

            self.assertFalse(result.ok)
            rendered = "\n".join(item.render() for item in result.findings)
            self.assertIn("PRIVATE_MARKER_", rendered)
            self.assertIn("<redacted-path:", rendered)
            self.assertNotIn(private_marker, rendered)

    def test_repository_scan_redacts_sensitive_content_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            sensitive_name = "private-client-alpha.md"
            credential_value = "sk-" + "C" * 24
            (root / sensitive_name).write_text(credential_value + "\n", encoding="utf-8")
            self.commit_all(root, "add fixture")

            result = scan_repository(root, include_history=True)

            self.assertFalse(result.ok)
            rendered = "\n".join(item.render() for item in result.findings)
            self.assertIn("<redacted-path:", rendered)
            self.assertNotIn(sensitive_name, rendered)

    def test_redacted_paths_are_opaque_and_distinguishable(self) -> None:
        first = redact_path("private-client-alpha.md")
        second = redact_path("private-client-beta.md")

        self.assertNotEqual(first, second)
        self.assertEqual(first, redact_path("private-client-alpha.md"))
        self.assertNotIn("private-client", first)

    def test_history_scan_fails_closed_for_oversized_blob(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            sensitive_name = "large-private-record.txt"
            (root / sensitive_name).write_text("x" * 32, encoding="utf-8")
            self.commit_all(root, "add oversized fixture")
            (root / sensitive_name).unlink()
            self.commit_all(root, "remove oversized fixture")

            with mock.patch("pos_boilerplate.secrets.MAX_SCANNED_BYTES", 16):
                worktree_result = scan_repository(root, include_history=False)
                result = scan_repository(root, include_history=True)

            self.assertTrue(worktree_result.ok)
            self.assertFalse(result.ok)
            self.assertTrue(
                any(
                    item.rule_id == "UNSCANNABLE_CONTENT"
                    and item.path == redact_path(sensitive_name)
                    and item.scope.startswith("history:")
                    for item in result.findings
                )
            )
            self.assertNotIn(
                sensitive_name,
                "\n".join(item.render() for item in result.findings),
            )

    def test_history_scan_detects_absolute_private_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "notes.md").write_text(
                "Read /" + "Users/release-audit/private.txt\n",
                encoding="utf-8",
            )
            self.commit_all(root, "add path fixture")

            result = scan_repository(root, include_history=True)

            self.assertFalse(result.ok)
            self.assertIn(
                "ABSOLUTE_USER_PATH",
                {item.rule_id for item in result.findings},
            )

    def test_scan_detects_bare_absolute_private_home_path(self) -> None:
        findings = scan_text("Home: /" + "Users/private-owner", "notes.md")

        self.assertIn("ABSOLUTE_USER_PATH", {item.rule_id for item in findings})

    def test_absolute_home_path_policy_covers_private_and_placeholder_paths(self) -> None:
        cases = (
            ("/" + "Users/private-owner/file.md", True),
            ("/" + "home/private-owner/file.md", True),
            ("/" + "home/user/file.md", True),
            ("/" + "Users/jörg/file.md", True),
            ("/Users/example/file.md", False),
            ("/home/your_user/file.md", False),
            ("GET /users/@me", False),
        )
        for text, should_block in cases:
            with self.subTest(text=text):
                rule_ids = {item.rule_id for item in scan_text(text, "notes.md")}
                self.assertEqual(should_block, "ABSOLUTE_USER_PATH" in rule_ids)

    def test_private_markers_use_unicode_normalization(self) -> None:
        findings = scan_text(
            "Client: Cafe\N{COMBINING ACUTE ACCENT}",
            "notes.md",
            private_markers=("Café",),
        )

        self.assertTrue(any(item.rule_id.startswith("PRIVATE_MARKER_") for item in findings))

    def test_worktree_file_reads_are_bounded_before_decode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "large.bin"
            with path.open("wb") as handle:
                handle.truncate(MAX_SCANNED_BYTES * 2)

            content = _read_bounded_file(path)

            self.assertEqual(MAX_SCANNED_BYTES + 1, len(content))

    def test_cli_returns_failure_without_printing_secret_value(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            credential_value = "github_" + "pat_" + "A" * 40
            (root / "credential.txt").write_text(
                credential_value + "\n", encoding="utf-8"
            )
            self.commit_all(root, "credential fixture")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = main(
                    ["secret-scan", "--repository", str(root), "--history"]
                )

            self.assertEqual(4, exit_code)
            self.assertIn("GITHUB_TOKEN", stderr.getvalue())
            self.assertNotIn(credential_value, stderr.getvalue())

    def test_cli_loads_private_marker_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "README.md").write_text("Public Product\n", encoding="utf-8")
            self.commit_all(root, "initial")
            markers = root / "markers.json"
            markers.write_text(
                json.dumps(["Public Product", "Private Person"]), encoding="utf-8"
            )
            safe = root / "safe.json"
            safe.write_text(json.dumps(["Public Product"]), encoding="utf-8")

            exit_code = main(
                [
                    "secret-scan",
                    "--repository",
                    str(root),
                    "--history",
                    "--private-markers",
                    str(markers),
                    "--public-safe-terms",
                    str(safe),
                ]
            )

            self.assertEqual(0, exit_code)

    def test_cli_rejects_fully_neutralized_private_markers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "README.md").write_text("Public\n", encoding="utf-8")
            self.commit_all(root, "public fixture")
            markers = root / "markers.json"
            safe_terms = root / "safe-terms.json"
            markers.write_text(json.dumps(["Public Term"]), encoding="utf-8")
            safe_terms.write_text(json.dumps(["public term"]), encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = main(
                    [
                        "secret-scan",
                        "--repository",
                        str(root),
                        "--private-markers",
                        str(markers),
                        "--public-safe-terms",
                        str(safe_terms),
                    ]
                )

            self.assertEqual(4, exit_code)
            self.assertIn("no effective rules", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
