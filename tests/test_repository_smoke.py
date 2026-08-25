from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
import re
from pathlib import Path

from pos_boilerplate.audit import audit_build
from pos_boilerplate.install import InstallConfig, InstallError, install_personalos
from pos_boilerplate.sync import BOILERPLATE_VERSION


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class RepositorySmokeTests(unittest.TestCase):
    def test_repository_build_manifest_and_links_are_valid(self) -> None:
        markers_path = REPOSITORY_ROOT / "policy/private-markers.local.json"
        if os.environ.get("POS_RELEASE_AUDIT") == "1" and not markers_path.is_file():
            self.fail("Release audit requires policy/private-markers.local.json")
        markers = json.loads(markers_path.read_text(encoding="utf-8")) if markers_path.is_file() else []
        public_safe_terms = tuple(
            json.loads((REPOSITORY_ROOT / "policy/public-safe-terms.json").read_text(encoding="utf-8"))
        )
        result = audit_build(REPOSITORY_ROOT, markers, public_safe_terms)
        self.assertTrue(result.ok, result.findings)

    def test_blueprints_match_their_generated_core_files(self) -> None:
        blueprints = REPOSITORY_ROOT / "blueprints"
        for source in sorted(path for path in blueprints.rglob("*") if path.is_file()):
            relative = source.relative_to(blueprints)
            if relative.parts[0] == "_modules":
                generated = REPOSITORY_ROOT / "modules" / Path(*relative.parts[1:])
                self.assertTrue(generated.is_file(), f"Missing generated module blueprint: {relative}")
                self.assertEqual(source.read_bytes(), generated.read_bytes(), str(relative))
                continue
            if relative.parts[0] == "_static":
                relative = Path(*relative.parts[1:])
            generated = REPOSITORY_ROOT / "core" / relative
            if not generated.is_file():
                candidates = list((REPOSITORY_ROOT / "modules").glob(f"*/payload/{relative}"))
                self.assertEqual(1, len(candidates), f"Missing or ambiguous generated blueprint: {relative}")
                generated = candidates[0]
            self.assertEqual(source.read_bytes(), generated.read_bytes(), str(relative))

    def test_reference_is_the_exact_composition_of_core_and_all_modules(self) -> None:
        expected: dict[str, bytes] = {}
        for path in sorted((REPOSITORY_ROOT / "core").rglob("*")):
            if path.is_file():
                expected[path.relative_to(REPOSITORY_ROOT / "core").as_posix()] = path.read_bytes()
        for payload in sorted((REPOSITORY_ROOT / "modules").glob("*/payload")):
            for path in sorted(payload.rglob("*")):
                if path.is_file():
                    relative = path.relative_to(payload).as_posix()
                    self.assertNotIn(relative, expected, f"Module collision: {relative}")
                    expected[relative] = path.read_bytes()
        actual = {
            path.relative_to(REPOSITORY_ROOT / "reference").as_posix(): path.read_bytes()
            for path in (REPOSITORY_ROOT / "reference").rglob("*")
            if path.is_file()
        }
        self.assertEqual(expected, actual)

    def test_core_contains_every_mandatory_domain(self) -> None:
        mandatory = {
            "inbox", "identity", "people", "companies", "projects", "operations",
            "decisions", "knowledge", "interactions", "daily", "system",
        }
        self.assertEqual(set(), {name for name in mandatory if not (REPOSITORY_ROOT / "core" / name).is_dir()})
        self.assertEqual(
            set(),
            {name for name in {"business", "content", "finance", "health"} if (REPOSITORY_ROOT / "core" / name).exists()},
        )

    def test_onboarding_starts_with_four_choices_and_a_write_gate(self) -> None:
        onboarding = (REPOSITORY_ROOT / "onboarding/agent-onboarding.md").read_text(encoding="utf-8")
        self.assertIn("1. vollständiges PersonalOS", onboarding)
        self.assertIn("2. Kern mit ausgewählten Modulen", onboarding)
        self.assertIn("3. nur verstehen", onboarding)
        self.assertIn("4. einzelne Teile übernehmen", onboarding)
        self.assertIn("Warte auf die Wahl", onboarding)
        self.assertIn("warte auf die Bestätigung", onboarding)
        self.assertIn("Bei Weg 3 schreibt der Agent nichts", onboarding)
        self.assertTrue((REPOSITORY_ROOT / "LICENSE").read_text().startswith("MIT License"))

    def test_public_release_documents_state_scope_and_support_boundaries(self) -> None:
        required = {
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CODE_OF_CONDUCT.md",
            "CHANGELOG.md",
            "SUPPORT.md",
            "docs/releasing.md",
            "docs/releases/v0.1.0.md",
            "docs/philosophy.md",
            "docs/system-map.md",
            "docs/external-systems-and-sync.md",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/pull_request_template.md",
            ".github/workflows/ci.yml",
        }
        self.assertEqual(
            set(),
            {path for path in required if not (REPOSITORY_ROOT / path).is_file()},
        )
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        product_contract = (REPOSITORY_ROOT / "docs/product-contract.md").read_text(
            encoding="utf-8"
        )
        release = (REPOSITORY_ROOT / "docs/releasing.md").read_text(encoding="utf-8")
        workflow = (REPOSITORY_ROOT / ".github/workflows/ci.yml").read_text(
            encoding="utf-8"
        )
        privacy_workflow = (REPOSITORY_ROOT / ".github/workflows/privacy.yml").read_text(
            encoding="utf-8"
        )
        for content in (
            readme,
            product_contract,
            (REPOSITORY_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
            (REPOSITORY_ROOT / "docs/releases/v0.1.0.md").read_text(encoding="utf-8"),
        ):
            self.assertNotIn("datenschutzsicher", content.casefold())
            self.assertNotIn("datenschutzbereinigt", content.casefold())
        self.assertIn("1:1 dieselbe Systembasis", readme)
        self.assertIn("nicht dieselbe betriebsbereite Laufzeit", readme)
        self.assertIn("bewusste Maintainer-Freigabe", release)
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn("secret-scan --repository . --history", workflow)
        self.assertIn("pull_request_target:", privacy_workflow)
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", privacy_workflow)
        self.assertIn("python -m pip install .", privacy_workflow)
        self.assertIn("POS_PRIVATE_MARKERS_JSON", privacy_workflow)
        self.assertIn("has no effective rules", privacy_workflow)
        self.assertIn("Fetch pull request as data", privacy_workflow)
        self.assertIn("Scan pull request objects with trusted code", privacy_workflow)
        self.assertNotIn("actions/checkout@v7\n        with:\n          ref: ${{ github.event.pull_request", privacy_workflow)

    def test_documented_python_check_invocations_resolve(self) -> None:
        missing: list[str] = []
        for document in sorted((REPOSITORY_ROOT / "core/system/checks").rglob("*.md")):
            text = document.read_text(encoding="utf-8")
            for relative in re.findall(r"python3\s+((?:system|skills)/[^\s`]+\.py)", text):
                if "<" in relative or "{{" in relative:
                    continue
                if not (REPOSITORY_ROOT / "core" / relative).is_file():
                    missing.append(f"{document.relative_to(REPOSITORY_ROOT)} -> {relative}")
            for test_root, pattern in re.findall(
                r"python3 -m unittest discover -s ([^\s`]+) -p ['\"]([^'\"]+)['\"]",
                text,
            ):
                target = REPOSITORY_ROOT / "core" / test_root
                if not target.is_dir() or not any(target.glob(pattern)):
                    missing.append(
                        f"{document.relative_to(REPOSITORY_ROOT)} -> {test_root}/{pattern}"
                    )
        self.assertEqual([], missing)

    def test_agent_entry_is_prominent_linked_and_safe(self) -> None:
        prompt = (
            "Lies zuerst AGENTS.md und START-HERE.md in diesem Repository. "
            "Zeige mir danach die vier möglichen Wege, hilf mir bei der Auswahl "
            "und ändere noch keine Dateien."
        )
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        start_here = (REPOSITORY_ROOT / "START-HERE.md").read_text(encoding="utf-8")
        agents = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn(prompt, readme)
        self.assertIn(prompt, start_here)
        self.assertLess(readme.index("## In 30 Sekunden"), readme.index("## Was PersonalOS ist"))
        for link in (
            "docs/philosophy.md",
            "docs/system-map.md",
            "docs/external-systems-and-sync.md",
        ):
            self.assertIn(link, readme)
            self.assertIn(link, agents)

        public_entry_documents = (
            "README.md",
            "START-HERE.md",
            "AGENTS.md",
            "onboarding/agent-onboarding.md",
            "docs/philosophy.md",
            "docs/system-map.md",
            "docs/external-systems-and-sync.md",
            "docs/product-contract.md",
            "docs/coverage.md",
            "docs/update-model.md",
            "docs/releases/v0.1.0.md",
            "CHANGELOG.md",
        )
        for relative in public_entry_documents:
            content = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("—", content, relative)
            self.assertNotIn("–", content, relative)

    def test_multi_host_contract_has_one_automated_git_writer(self) -> None:
        module_readme = (REPOSITORY_ROOT / "modules/multi-host/README.md").read_text(
            encoding="utf-8"
        )
        runbook = (
            REPOSITORY_ROOT
            / "modules/multi-host/payload/system/runbooks/modules/multi-host.md"
        ).read_text(encoding="utf-8")
        self.assertIn("genau einen automatischen Git-Writer", module_readme)
        self.assertIn("genau einen automatischen Git-Writer", runbook)

    def test_package_and_manifest_versions_match(self) -> None:
        project = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        manifest = json.loads((REPOSITORY_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(BOILERPLATE_VERSION, project["project"]["version"])
        self.assertEqual(BOILERPLATE_VERSION, manifest["boilerplate_version"])

    def test_repository_installs_as_a_valid_clean_personalos(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "PersonalOS"
            values = json.loads(
                (REPOSITORY_ROOT / "examples/install-values.example.json").read_text(
                    encoding="utf-8"
                )
            )
            values["install_date"] = "2026-08-23"
            values["user_name"] = "Ada O'Neil Example"

            install_personalos(
                InstallConfig(
                    build_root=REPOSITORY_ROOT,
                    destination=destination,
                    modules=None,
                    values=values,
                )
            )

            markdown_files = sorted(
                path.relative_to(destination).as_posix()
                for path in destination.rglob("*.md")
                if path.name != "CLAUDE.md"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "system/data-model/scripts/pos_v1.py",
                    "validate",
                    "--files",
                    *markdown_files,
                    "--json",
                ],
                cwd=destination,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("pass", json.loads(result.stdout)["status"])

            compiled = subprocess.run(
                [sys.executable, "-m", "compileall", "-q", "."],
                cwd=destination,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, compiled.returncode, compiled.stdout + compiled.stderr)

            registry_tests = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "system/data-model/tests",
                    "-p",
                    "test_registry_contract.py",
                ],
                cwd=destination,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                0,
                registry_tests.returncode,
                registry_tests.stdout + registry_tests.stderr,
            )

            resolvable = subprocess.run(
                [
                    sys.executable,
                    "system/checks/system/scripts/check-resolvable.py",
                ],
                cwd=destination,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, resolvable.returncode, resolvable.stdout + resolvable.stderr)
            self.assertIn("errors: 0", resolvable.stdout)

    def test_real_core_and_selected_module_installs_are_resolvable(self) -> None:
        values = json.loads(
            (REPOSITORY_ROOT / "examples/install-values.example.json").read_text(encoding="utf-8")
        )
        values["install_date"] = "2026-08-23"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for name, modules in (("core", ()), ("selected", ("content", "codex"))):
                destination = root / name
                install_personalos(
                    InstallConfig(REPOSITORY_ROOT, destination, modules, values)
                )
                result = subprocess.run(
                    [sys.executable, "system/checks/system/scripts/check-resolvable.py"],
                    cwd=destination,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("errors: 0", result.stdout)

    def test_real_install_rejects_incomplete_personal_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(InstallError, "Missing install values"):
                install_personalos(
                    InstallConfig(
                        REPOSITORY_ROOT,
                        Path(temp_dir) / "PersonalOS",
                        (),
                        {"user_name": "Alex"},
                    )
                )


if __name__ == "__main__":
    unittest.main()
