from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from pos_boilerplate.cli import main
from pos_boilerplate.install import (
    InstallConfig,
    InstallError,
    _normalize_installed_text,
    install_personalos,
)
from pos_boilerplate.sync import BUILD_CONTRACT
from pos_boilerplate.target import hand_over


class InstallTests(unittest.TestCase):
    def test_install_refuses_private_target_inside_public_build(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            build = self.make_build(Path(temp))
            before = {p.relative_to(build).as_posix(): p.read_bytes() for p in build.rglob("*") if p.is_file()}
            for target in (build, build / "PersonalOS", build / "nested/PersonalOS"):
                with self.subTest(target=target), self.assertRaisesRegex(InstallError, "outside"):
                    install_personalos(InstallConfig(build, target, (), {"user_name": "Private Example"}))
            after = {p.relative_to(build).as_posix(): p.read_bytes() for p in build.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            self.assertFalse((build / "PersonalOS").exists())
            self.assertFalse((build / "nested").exists())

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

    def update_payload(self, build: Path, relative: str, content: bytes) -> None:
        manifest_path = build / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for prefix in ("core", "reference"):
            target = build / prefix / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            entry_path = f"{prefix}/{relative}"
            entry = next(
                (item for item in manifest["managed_files"] if item["path"] == entry_path),
                None,
            )
            if entry is None:
                entry = {"path": entry_path, "source_path": "test-fixture", "rule_id": "test-fixture"}
                manifest["managed_files"].append(entry)
            entry["sha256"] = hashlib.sha256(content).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8", newline="\n")

    def test_install_normalizes_crlf_once_and_preserves_blank_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            self.update_payload(build, "USER.md", b"Name: {{user_name}}\r\n\r\nTail\r\n")
            destination = root / "PersonalOS"

            install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertEqual((destination / "USER.md").read_bytes(), b"Name: Alex\n\nTail\n")
            self.assertEqual((destination / "script.py").read_bytes(), b'MESSAGE = "public"\n')

    def test_receipt_records_final_bytes_without_identity_or_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "private-destination"

            def rebuild(staging: Path) -> None:
                (staging / "script.py").write_bytes(b"# rebuilt\n")
                (staging / "registry.json").write_bytes(b'{"records": []}\n')

            with mock.patch("pos_boilerplate.install.rebuild_installed_data_model", side_effect=rebuild):
                install_personalos(
                    InstallConfig(build, destination, ("example",), {"user_name": "Sensitive Owner"})
                )

            receipt_text = (destination / ".personalos-install.json").read_text(encoding="utf-8")
            receipt = json.loads(receipt_text)
            self.assertEqual(receipt["schema_version"], 1)
            self.assertEqual(receipt["boilerplate_version"], "0.1.0")
            self.assertEqual(receipt["source_revision"], "a" * 40)
            self.assertEqual(receipt["source_date"], "2026-08-23T15:51:49+02:00")
            self.assertEqual(receipt["modules"], ["example"])
            self.assertNotIn("Sensitive Owner", receipt_text)
            self.assertNotIn("private-destination", receipt_text)
            self.assertNotIn(str(root), receipt_text)
            managed = {entry["path"]: entry["sha256"] for entry in receipt["managed_files"]}
            expected_paths = {
                file.relative_to(destination).as_posix()
                for file in destination.rglob("*")
                if file.is_file() and file.name != ".personalos-install.json"
            }
            self.assertEqual(set(managed), expected_paths)
            self.assertIn("registry.json", managed)
            self.assertNotIn(".personalos-install.json", managed)
            for relative, digest in managed.items():
                self.assertEqual(digest, hashlib.sha256((destination / relative).read_bytes()).hexdigest())

    def test_registry_rebuild_keeps_lf_text_and_binary_bytes_without_bytecode(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            self.update_payload(
                build,
                "system/data-model/scripts/registry_helper.py",
                b"RESULT = b'registry rebuilt\\r\\n\\r\\nfinished\\r\\n'\n"
                b"BINARY = b'\\x00binary\\r\\n'\n"
                b"RAW = b'\\xffbinary\\r\\n'\n",
            )
            self.update_payload(
                build,
                "system/data-model/scripts/pos_v1.py",
                b"import sys\nfrom pathlib import Path\nimport registry_helper\n"
                b"root = Path(sys.argv[sys.argv.index('--root') + 1])\n"
                b"(root / 'registry.json').write_bytes(registry_helper.RESULT)\n"
                b"(root / 'registry.bin').write_bytes(registry_helper.BINARY)\n"
                b"(root / 'raw.bin').write_bytes(registry_helper.RAW)\n",
            )
            destination = root / "PersonalOS"
            # Exercise a real subprocess import even if the parent shell disables
            # bytecode writes or redirects them to a shared cache directory.
            with mock.patch.dict(os.environ, {"PYTHONDONTWRITEBYTECODE": "", "PYTHONPYCACHEPREFIX": ""}):
                install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            expected_files = {
                "registry.json": b"registry rebuilt\n\nfinished\n",
                "registry.bin": b"\x00binary\r\n",
                "raw.bin": b"\xffbinary\r\n",
            }
            for relative, content in expected_files.items():
                self.assertEqual((destination / relative).read_bytes(), content)
            self.assertEqual(list(destination.rglob("__pycache__")), [])
            self.assertEqual(list(destination.rglob("*.pyc")), [])
            receipt = json.loads((destination / ".personalos-install.json").read_text(encoding="utf-8"))
            managed_paths = {entry["path"] for entry in receipt["managed_files"]}
            self.assertIn("registry.json", managed_paths)
            self.assertFalse(any("__pycache__" in path or path.endswith(".pyc") for path in managed_paths))
            managed = {entry["path"]: entry["sha256"] for entry in receipt["managed_files"]}
            for relative, content in expected_files.items():
                self.assertEqual(managed[relative], hashlib.sha256(content).hexdigest())

    def test_install_rejects_reserved_receipt_payload_and_cleans_staging(self) -> None:
        for relative in (".personalos-install.json", ".PERSONALOS-INSTALL.JSON", ".personalos-install.json/payload"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                build = self.make_build(root)
                self.update_payload(build, relative, b"reserved\n")
                destination = root / "PersonalOS"
                destination.mkdir()

                with self.assertRaisesRegex(InstallError, "reserved"):
                    install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

                self.assertTrue(destination.is_dir())
                self.assertEqual(list(destination.iterdir()), [])
                self.assertEqual(list(root.glob(".PersonalOS-install-*")), [])

    def test_normalization_rejects_all_symlinks_before_writing_any_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            staging = root / "staging"
            staging.mkdir()
            first = staging / "a-first.md"
            first.write_bytes(b"unchanged before validation\r\n")
            outside = root / "outside.md"
            outside.write_bytes(b"outside content\r\n")
            try:
                (staging / "z-symlink.md").symlink_to(outside)
            except OSError as exc:
                if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                    self.skipTest("Windows runner lacks permission to create symlinks")
                raise

            with self.assertRaisesRegex(InstallError, "unsafe file"):
                _normalize_installed_text(staging)

            self.assertEqual(first.read_bytes(), b"unchanged before validation\r\n")
            self.assertEqual(outside.read_bytes(), b"outside content\r\n")

    def test_install_failure_preserves_empty_target_and_removes_staging(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"
            destination.mkdir()

            with mock.patch(
                "pos_boilerplate.install.rebuild_installed_data_model",
                side_effect=InstallError("Registry failed"),
            ), self.assertRaisesRegex(InstallError, "Registry failed"):
                install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertTrue(destination.is_dir())
            self.assertEqual(list(destination.iterdir()), [])
            self.assertEqual(list(root.glob(".PersonalOS-install-*")), [])

    def test_install_refuses_symlinked_target_without_changing_its_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            actual = root / "actual"
            actual.mkdir()
            destination = root / "PersonalOS"
            try:
                destination.symlink_to(actual, target_is_directory=True)
            except OSError as exc:
                if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                    self.skipTest("Windows runner lacks permission to create symlinks")
                raise

            with self.assertRaisesRegex(InstallError, "symlink"):
                install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertTrue(destination.is_symlink())
            self.assertEqual(list(actual.iterdir()), [])

    def test_install_preserves_files_added_to_destination_during_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"
            destination.mkdir()

            def rebuild(staging: Path) -> None:
                (destination / "mine.md").write_bytes(b"created while install was running\n")

            with mock.patch(
                "pos_boilerplate.install.rebuild_installed_data_model", side_effect=rebuild
            ), self.assertRaises(OSError):
                install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertEqual((destination / "mine.md").read_bytes(), b"created while install was running\n")
            self.assertEqual(list(destination.iterdir()), [destination / "mine.md"])
            self.assertEqual(list(root.glob(".PersonalOS-install-*")), [])

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

    def test_install_keeps_a_prepared_obsidian_vault_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"
            (destination / ".obsidian").mkdir(parents=True)
            (destination / ".obsidian/app.json").write_bytes(b'{"vault": "mine"}')
            (destination / ".DS_Store").write_bytes(b"finder")
            identity = os.stat(destination).st_ino

            install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertEqual((destination / ".obsidian/app.json").read_bytes(), b'{"vault": "mine"}')
            self.assertEqual((destination / ".DS_Store").read_bytes(), b"finder")
            self.assertIn("Name: Alex", (destination / "USER.md").read_text(encoding="utf-8"))
            self.assertEqual(os.stat(destination).st_ino, identity)
            receipt = (destination / ".personalos-install.json").read_text(encoding="utf-8")
            self.assertNotIn(".obsidian", receipt)
            self.assertNotIn(".DS_Store", receipt)
            self.assertEqual(list(root.glob(".PersonalOS-install-*")), [])

    def test_install_refuses_notes_next_to_a_prepared_vault(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = self.make_build(root)
            destination = root / "PersonalOS"
            (destination / ".obsidian").mkdir(parents=True)
            (destination / "note.md").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(InstallError, "not empty"):
                install_personalos(InstallConfig(build, destination, (), {"user_name": "Alex"}))

            self.assertEqual(sorted(p.name for p in destination.iterdir()), [".obsidian", "note.md"])
            self.assertEqual(list(root.glob(".PersonalOS-install-*")), [])

    def test_failed_handover_moves_installed_entries_back(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            staging = root / "staging"
            staging.mkdir()
            (staging / "AGENTS.md").write_text("a", encoding="utf-8")
            (staging / "USER.md").write_text("u", encoding="utf-8")
            destination = root / "PersonalOS"
            (destination / ".obsidian").mkdir(parents=True)
            real_replace = os.replace

            def flaky(source, target):
                if Path(source).name == "USER.md":
                    raise PermissionError("locked")
                real_replace(source, target)

            with mock.patch("pos_boilerplate.target.os.replace", side_effect=flaky), self.assertRaises(OSError):
                hand_over(staging, destination)

            self.assertEqual([p.name for p in destination.iterdir()], [".obsidian"])
            self.assertEqual(sorted(p.name for p in staging.iterdir()), ["AGENTS.md", "USER.md"])

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
                (build / relative).write_text(content, encoding="utf-8", newline="\n")
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
