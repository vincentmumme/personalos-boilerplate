from __future__ import annotations

import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from pos_boilerplate.audit import audit_build
from pos_boilerplate.cli import main
from pos_boilerplate.sync import BUILD_CONTRACT


class AuditTests(unittest.TestCase):
    def make_build(self, root: Path, content: str = "# Index\n") -> Path:
        build = root / "build"
        (build / "core").mkdir(parents=True)
        path = build / "core/INDEX.md"
        path.write_text(content, encoding="utf-8")
        (build / "reference").mkdir(parents=True)
        reference_path = build / "reference/INDEX.md"
        reference_path.write_text(content, encoding="utf-8")
        (build / "modules").mkdir(parents=True)
        catalog_path = build / "modules/catalog.json"
        catalog_path.write_text(
            json.dumps({"schema_version": 1, "default_enabled": [], "modules": []}),
            encoding="utf-8",
        )
        manifest = {
            "schema_version": 2,
            "build_contract": BUILD_CONTRACT,
            "boilerplate_version": "0.1.0",
            "source_revision": "a" * 40,
            "source_date": "2026-08-23T15:51:49+02:00",
            "counts": {"render": 1},
            "managed_files": [
                {
                    "path": "core/INDEX.md",
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "source_path": "INDEX.md",
                    "rule_id": "root-index",
                },
                {
                    "path": "reference/INDEX.md",
                    "sha256": hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                    "source_path": "generated:core/INDEX.md",
                    "rule_id": "reference-composition",
                },
                {
                    "path": "modules/catalog.json",
                    "sha256": hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
                    "source_path": "generated:module-catalog",
                    "rule_id": "module-catalog",
                },
            ],
        }
        (build / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return build

    def test_clean_build_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir))
            (build / "README.md").write_text("Repository documentation", encoding="utf-8")
            result = audit_build(build, private_markers=[])

            self.assertTrue(result.ok)
            self.assertEqual(result.findings, ())

    def test_manifest_hash_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir))
            (build / "core/INDEX.md").write_text("changed", encoding="utf-8")

            result = audit_build(build, private_markers=[])

            self.assertFalse(result.ok)
            self.assertIn("manifest-hash-mismatch", {finding.code for finding in result.findings})

    def test_broken_internal_link_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir), "See [[missing-record]].\n")

            result = audit_build(build, private_markers=[])

            self.assertFalse(result.ok)
            self.assertIn("broken-wikilink", {finding.code for finding in result.findings})

    def test_privacy_scan_covers_manifest_paths_and_fixture_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            fixture = build / "examples/fixtures/private.fixture"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("Private Person", encoding="utf-8")
            manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
            manifest["managed_files"].append(
                {
                    "path": "examples/fixtures/private.fixture",
                    "sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
                    "source_path": "fixtures/private.fixture",
                    "rule_id": "fixture",
                }
            )
            (build / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            result = audit_build(build, private_markers=["Private Person"])

            privacy_paths = {
                finding.path for finding in result.findings if finding.code == "privacy-marker"
            }
            self.assertEqual(1, len(privacy_paths))
            self.assertTrue(next(iter(privacy_paths)).startswith("<redacted-path:"))
            self.assertNotIn(
                "private.fixture",
                "\n".join(f"{item.path}\t{item.detail}" for item in result.findings),
            )

    def test_audit_cli_redacts_sensitive_filenames(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            sensitive_name = "private-client-alpha.fixture"
            fixture = build / "examples/fixtures" / sensitive_name
            fixture.parent.mkdir(parents=True)
            fixture.write_text("Private Person", encoding="utf-8")
            manifest_path = build / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["managed_files"].append(
                {
                    "path": f"examples/fixtures/{sensitive_name}",
                    "sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
                    "source_path": "fixtures/redacted.fixture",
                    "rule_id": "fixture",
                }
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            unmanaged_name = "private-client-unmanaged.md"
            (build / "core" / unmanaged_name).write_text("clean\n", encoding="utf-8")
            markers = root / "markers.json"
            markers.write_text(json.dumps(["Private Person"]), encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = main(
                    [
                        "audit",
                        "--build",
                        str(build),
                        "--private-markers",
                        str(markers),
                    ]
                )

            self.assertEqual(3, exit_code)
            self.assertIn("<redacted-path:", stderr.getvalue())
            self.assertNotIn(sensitive_name, stderr.getvalue())
            self.assertNotIn(unmanaged_name, stderr.getvalue())

    def test_audit_cli_rejects_fully_neutralized_private_markers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            markers = root / "markers.json"
            safe_terms = root / "safe-terms.json"
            markers.write_text(json.dumps(["Public Term"]), encoding="utf-8")
            safe_terms.write_text(json.dumps(["public term"]), encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = main(
                    [
                        "audit",
                        "--build",
                        str(build),
                        "--private-markers",
                        str(markers),
                        "--public-safe-terms",
                        str(safe_terms),
                    ]
                )

            self.assertEqual(3, exit_code)
            self.assertIn("no effective rules", stderr.getvalue())

    def test_public_safe_term_only_exempts_the_named_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir), "# Hermes\nPrivate Person\n")

            result = audit_build(
                build,
                private_markers=["Hermes", "Private Person"],
                public_safe_terms=("Hermes",),
            )

            details = {item.detail for item in result.findings if item.code == "privacy-marker"}
            self.assertEqual(1, len(details))

    def test_reference_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir))
            reference = build / "reference/INDEX.md"
            reference.write_text("changed\n", encoding="utf-8")
            manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
            for item in manifest["managed_files"]:
                if item["path"] == "reference/INDEX.md":
                    item["sha256"] = hashlib.sha256(reference.read_bytes()).hexdigest()
            (build / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            result = audit_build(build, [])

            self.assertIn("reference-content-mismatch", {item.code for item in result.findings})

    def test_incomplete_v2_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir))
            manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
            del manifest["source_date"]
            (build / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            result = audit_build(build, [])

            self.assertIn("invalid-manifest", {item.code for item in result.findings})

    def test_module_catalog_must_match_payload_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            build = self.make_build(Path(temp_dir))
            (build / "modules/undeclared/payload").mkdir(parents=True)

            result = audit_build(build, [])

            self.assertIn("invalid-module-catalog", {item.code for item in result.findings})

    def test_git_worktree_audit_scans_python_files_for_private_home_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repository = self.make_build(root)
            (repository / "helper.py").write_text(
                'PATH = "/' + 'Users/release-audit/private.txt"\n',
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.email", "test@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repository), "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(["git", "-C", str(repository), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(repository), "commit", "-qm", "fixture"], check=True)
            worktree = root / "worktree"
            subprocess.run(
                ["git", "-C", str(repository), "worktree", "add", "-q", str(worktree)],
                check=True,
            )

            result = audit_build(worktree, [])

            self.assertIn(
                "absolute-user-path",
                {item.detail for item in result.findings if item.code == "privacy-marker"},
            )


if __name__ == "__main__":
    unittest.main()
