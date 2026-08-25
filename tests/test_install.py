from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import uuid
from pathlib import Path

from pos_boilerplate.cli import main
from pos_boilerplate.install import InstallConfig, InstallError, install_personalos
from pos_boilerplate.sync import BUILD_CONTRACT


class InstallTests(unittest.TestCase):
    def make_build(self, root: Path) -> Path:
        build = root / "build"
        (build / "core").mkdir(parents=True)
        (build / "core/USER.md").write_text(
            "Name: {{user_name}}\nID: {{id_user}}\nRecord date: {{date}}\n",
            encoding="utf-8",
        )
        (build / "core/script.py").write_text(
            'MESSAGE = "public"\n',
            encoding="utf-8",
        )
        (build / "core/hook").write_text(
            "#!/bin/sh\necho public\n",
            encoding="utf-8",
        )
        (build / "core/decisions/{{install_year}}").mkdir(parents=True)
        (build / "core/decisions/{{install_year}}/{{install_date}}-adopt.md").write_text(
            "Decided: {{install_date}}\n",
            encoding="utf-8",
        )
        (build / "modules/example/payload/skills/example").mkdir(parents=True)
        (build / "modules/example/payload/skills/example/SKILL.md").write_text(
            "Root: {{personalos_root}}\n",
            encoding="utf-8",
        )
        (build / "modules/second/payload/system/runbooks/modules").mkdir(parents=True)
        (build / "modules/second/payload/system/runbooks/modules/second.md").write_text(
            "# Second\n",
            encoding="utf-8",
        )
        catalog = {
            "schema_version": 1,
            "default_enabled": [],
            "modules": [
                {"id": "example", "kind": "extension", "title": "Example", "entry": "skills/example/SKILL"},
                {"id": "second", "kind": "extension", "title": "Second", "entry": "system/runbooks/modules/second"},
            ],
        }
        (build / "modules/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        reference = build / "reference"
        for source_root in (build / "core", build / "modules/example/payload", build / "modules/second/payload"):
            for source in source_root.rglob("*"):
                if not source.is_file():
                    continue
                relative = source.relative_to(source_root)
                target = reference / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
        managed = []
        for source in sorted(
            [path for root_path in (build / "core", build / "modules/example/payload", build / "modules/second/payload", reference) for path in root_path.rglob("*") if path.is_file()]
            + [build / "modules/catalog.json"]
        ):
            managed.append(
                {
                    "path": source.relative_to(build).as_posix(),
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "source_path": "test-fixture",
                    "rule_id": "test-fixture",
                }
            )
        (build / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "build_contract": BUILD_CONTRACT,
                    "boilerplate_version": "0.1.0",
                    "source_revision": "a" * 40,
                    "source_date": "2026-08-23T15:51:49+02:00",
                    "counts": {"render": 1},
                    "managed_files": managed,
                }
            ),
            encoding="utf-8",
        )
        return build

    def test_install_renders_identity_values_and_selected_modules(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"

            result = install_personalos(
                InstallConfig(
                    build_root=build,
                    destination=destination,
                    modules=("example",),
                    values={
                        "user_name": "Alex Example",
                        "install_date": "2026-08-23",
                    },
                )
            )

            user = (destination / "USER.md").read_text(encoding="utf-8")
            self.assertIn("Name: Alex Example", user)
            self.assertNotIn("{{id_user}}", user)
            rendered_id = user.split("ID: ", 1)[1].splitlines()[0]
            self.assertEqual(7, uuid.UUID(rendered_id).version)
            self.assertEqual(uuid.RFC_4122, uuid.UUID(rendered_id).variant)
            self.assertIn("Record date: {{date}}", user)
            self.assertEqual(
                (destination / "skills/example/SKILL.md").read_text(encoding="utf-8"),
                f"Root: {destination}\n",
            )
            self.assertEqual(result.modules, ("example",))
            self.assertEqual(
                (destination / "decisions/2026/2026-08-23-adopt.md").read_text(
                    encoding="utf-8"
                ),
                "Decided: 2026-08-23\n",
            )

    def test_install_refuses_nonempty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"
            destination.mkdir()
            (destination / "mine.md").write_text("keep", encoding="utf-8")

            with self.assertRaises(InstallError):
                install_personalos(
                    InstallConfig(
                        build_root=build,
                        destination=destination,
                        modules=(),
                        values={"user_name": "Alex"},
                    )
                )

            self.assertEqual((destination / "mine.md").read_text(), "keep")

    def test_install_rejects_unknown_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)

            with self.assertRaises(InstallError):
                install_personalos(
                    InstallConfig(
                        build_root=build,
                        destination=root / "PersonalOS",
                        modules=("missing",),
                        values={"user_name": "Alex"},
                    )
                )

    def test_install_rejects_module_traversal_and_inconsistent_date(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            with self.assertRaises(InstallError):
                install_personalos(
                    InstallConfig(build, root / "one", ("../example",), {})
                )
            with self.assertRaises(InstallError):
                install_personalos(
                    InstallConfig(
                        build,
                        root / "two",
                        (),
                        {"install_date": "not-a-date", "install_year": "2026"},
                    )
                )
            with self.assertRaises(InstallError):
                install_personalos(
                    InstallConfig(
                        build,
                        root / "three",
                        (),
                        {"install_date": "2026-02-31", "install_year": "2026"},
                    )
                )
            for index, invalid_date in enumerate(("20260825", "2026-W35-2"), start=4):
                with self.subTest(invalid_date=invalid_date), self.assertRaises(InstallError):
                    install_personalos(
                        InstallConfig(
                            build,
                            root / str(index),
                            (),
                            {"install_date": invalid_date, "install_year": "2026"},
                        )
                    )

    def test_install_rejects_placeholders_in_executable_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            content = '#!/bin/sh\necho "{{user_name}}"\n'
            for relative in ("core/hook", "reference/hook"):
                (build / relative).write_text(content, encoding="utf-8")
            manifest_path = build / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for item in manifest["managed_files"]:
                if item["path"] in {"core/hook", "reference/hook"}:
                    item["sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(InstallError, "executable template"):
                install_personalos(
                    InstallConfig(
                        build,
                        root / "PersonalOS",
                        (),
                        {"user_name": "Ada Example"},
                    )
                )

    def test_install_rejects_unsafe_human_identity_characters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)

            with self.assertRaisesRegex(InstallError, "Unsafe characters in user_name"):
                install_personalos(
                    InstallConfig(
                        build,
                        root / "PersonalOS",
                        (),
                        {"user_name": 'Ada "Ace" Example'},
                    )
                )

            with self.assertRaisesRegex(InstallError, "Invalid slug in user_slug"):
                install_personalos(
                    InstallConfig(
                        build,
                        root / "UnsafeSlug",
                        (),
                        {"user_name": "Ada Example", "user_slug": "../../private"},
                    )
                )

    def test_install_all_modules_builds_the_complete_reference_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"

            result = install_personalos(
                InstallConfig(build, destination, None, {"user_name": "Alex"})
            )

            self.assertEqual(result.modules, ("example", "second"))
            self.assertTrue((destination / "skills/example/SKILL.md").is_file())
            self.assertTrue((destination / "system/runbooks/modules/second.md").is_file())
            module_index = (destination / "system/runbooks/modules/index.md")
            if module_index.is_file():
                self.assertIn("[[skills/example/SKILL]]", module_index.read_text(encoding="utf-8"))

    def test_repeated_module_selection_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)

            result = install_personalos(
                InstallConfig(build, root / "PersonalOS", ("example", "example"), {"user_name": "Alex"})
            )

            self.assertEqual(("example",), result.modules)

    def test_install_rejects_tampered_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            (build / "core/USER.md").write_text("tampered\n", encoding="utf-8")

            with self.assertRaises(InstallError):
                install_personalos(InstallConfig(build, root / "PersonalOS", (), {"user_name": "Alex"}))

    def test_cli_all_modules_routes_to_complete_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            values = root / "values.json"
            values.write_text(json.dumps({"user_name": "Alex"}), encoding="utf-8")
            destination = root / "PersonalOS"

            self.assertEqual(
                0,
                main([
                    "install", "--build", str(build), "--destination", str(destination),
                    "--values", str(values), "--all-modules",
                ]),
            )
            self.assertTrue((destination / "system/runbooks/modules/second.md").is_file())


if __name__ == "__main__":
    unittest.main()
