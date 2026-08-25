from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pos_boilerplate.demo import DemoConfig, DemoError, build_demo


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class DemoTests(unittest.TestCase):
    def values(self) -> dict[str, str]:
        return json.loads(
            (REPOSITORY_ROOT / "examples/recording-demo/values.json").read_text(
                encoding="utf-8"
            )
        )

    def test_build_demo_installs_all_modules_and_applies_recording_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "PersonalOS-Demo"
            result = build_demo(
                DemoConfig(
                    build_root=REPOSITORY_ROOT,
                    destination=destination,
                    values=self.values(),
                    fixtures=REPOSITORY_ROOT / "examples/recording-demo/overlay",
                )
            )

            self.assertEqual(result.destination, destination)
            self.assertIn("hermes", result.modules)
            self.assertIn("external-signals", result.modules)
            user_context = (destination / "USER.md").read_text(encoding="utf-8")
            self.assertTrue(user_context.startswith("---\n"))
            self.assertIn("Vincent Mumme", user_context)
            self.assertTrue((destination / "companies/nordlicht-handel.md").is_file())
            self.assertTrue(
                (destination / "projects/personalos-masterclass/personalos-masterclass.md").is_file()
            )
            self.assertTrue((destination / "skills/analyse-call/SKILL.md").is_file())
            resolver = (destination / "skills/RESOLVER.md").read_text(encoding="utf-8")
            self.assertIn("skills/analyse-call/SKILL", resolver)
            discovery_packet = (
                destination
                / "interactions/meetings/2026/2026-08-22-nordlicht-discovery"
            )
            self.assertTrue(
                (
                    discovery_packet
                    / "evidence/01a02fb3-6e1d-720d-ac40-b805c8c5090f.md"
                ).is_file()
            )
            self.assertFalse((discovery_packet / "analysis").exists())

    def test_build_demo_rejects_a_nonempty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "PersonalOS-Demo"
            destination.mkdir()
            (destination / "keep.txt").write_text("user data", encoding="utf-8")

            with self.assertRaisesRegex(DemoError, "Zielordner ist nicht leer"):
                build_demo(
                    DemoConfig(
                        build_root=REPOSITORY_ROOT,
                        destination=destination,
                        values=self.values(),
                        fixtures=REPOSITORY_ROOT / "examples/recording-demo/overlay",
                    )
                )

    def test_build_demo_rejects_a_fixture_that_replaces_the_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            destination = temp_root / "PersonalOS-Demo"
            marker = temp_root / "runtime-executed.txt"
            runtime_fixture = (
                temp_root / "fixtures/system/data-model/scripts/pos_v1.py"
            )
            runtime_fixture.parent.mkdir(parents=True)
            runtime_fixture.write_text(
                f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(DemoError, "geschützten Pfad"):
                build_demo(
                    DemoConfig(
                        build_root=REPOSITORY_ROOT,
                        destination=destination,
                        values=self.values(),
                        fixtures=temp_root / "fixtures",
                    )
                )

            self.assertFalse(marker.exists())
            self.assertFalse(destination.exists())

    def test_build_demo_does_not_publish_invalid_markdown_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            destination = temp_root / "PersonalOS-Demo"
            invalid_record = temp_root / "fixtures/people/invalid.md"
            invalid_record.parent.mkdir(parents=True)
            invalid_record.write_text("not a registered record\n", encoding="utf-8")

            with self.assertRaisesRegex(DemoError, "Demo-Datensätze ist fehlgeschlagen"):
                build_demo(
                    DemoConfig(
                        build_root=REPOSITORY_ROOT,
                        destination=destination,
                        values=self.values(),
                        fixtures=temp_root / "fixtures",
                    )
                )

            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
