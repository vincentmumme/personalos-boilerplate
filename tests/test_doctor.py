from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfoNotFoundError

import test_install
from pos_boilerplate.cli import main
from pos_boilerplate.doctor import check_environment


class DoctorTests(unittest.TestCase):
    def test_new_destination_is_checked_without_creating_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = test_install.InstallTests().make_build(root)
            target = root / "nested" / "PersonalOS"
            result = check_environment(build, target)
            self.assertTrue(result.ok, result.to_dict())
            self.assertFalse(target.parent.exists())
            self.assertEqual("new", result.mode)

    def test_existing_mode_preserves_an_existing_system(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = test_install.InstallTests().make_build(root)
            target = root / "My notes"
            target.mkdir()
            sentinel = target / "private.md"
            sentinel.write_bytes(b"private source stays untouched")
            self.assertFalse(check_environment(build, target).ok)
            result = check_environment(build, target, mode="existing")
            self.assertTrue(result.ok, result.to_dict())
            self.assertEqual(b"private source stays untouched", sentinel.read_bytes())
            self.assertEqual([sentinel], list(target.iterdir()))
            self.assertNotIn("private source", json.dumps(result.to_dict()))

    def test_existing_mode_requires_a_real_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = test_install.InstallTests().make_build(root)
            self.assertFalse(check_environment(build, root / "missing", mode="existing").ok)
            target = root / "file"
            target.write_bytes(b"keep")
            self.assertFalse(check_environment(build, target, mode="existing").ok)

    def test_target_inside_distribution_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            build = test_install.InstallTests().make_build(Path(temp))
            result = check_environment(build, build / "new-target")
            self.assertFalse(result.ok)
            self.assertIn("destination-in-build", [item.code for item in result.checks])

    def test_build_integrity_failures_get_an_actionable_diagnosis(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = test_install.InstallTests().make_build(root)
            path = build / "core/USER.md"
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
            result = check_environment(build, root / "new")
            self.assertFalse(result.ok)
            failure = next(item for item in result.checks if item.code == "build-integrity")
            self.assertIn("manifest-hash-mismatch", failure.message)
            self.assertTrue(failure.remedy)
            self.assertFalse((root / "new").exists())

    def test_missing_timezone_data_is_a_blocker_with_repair(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            build = test_install.InstallTests().make_build(Path(temp))
            with mock.patch("pos_boilerplate.doctor.ZoneInfo", side_effect=ZoneInfoNotFoundError):
                result = check_environment(build, timezone_name="Europe/Berlin")
            failure = next(item for item in result.checks if item.code == "timezone")
            self.assertEqual("fail", failure.status)
            self.assertIn("tzdata", failure.remedy)

    def test_unknown_timezone_is_reported_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            build = test_install.InstallTests().make_build(Path(temp))
            result = check_environment(build, timezone_name="../wrong")
            self.assertFalse(result.ok)

    def test_zip_install_does_not_require_git(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            build = test_install.InstallTests().make_build(Path(temp))
            with mock.patch("pos_boilerplate.doctor.shutil.which", return_value=None):
                result = check_environment(build)
            self.assertTrue(result.ok, result.to_dict())
            self.assertEqual("warn", next(item for item in result.checks if item.code == "git").status)

    def test_invalid_build_is_a_structured_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["doctor", "--build", str(root), "--json"])
            self.assertEqual(2, code)
            self.assertFalse(json.loads(output.getvalue())["ok"])

    def test_cli_json_and_text_explain_results_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = test_install.InstallTests().make_build(root)
            target = root / "new"
            for output_flag in ([], ["--json"]):
                with self.subTest(output_flag=output_flag):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        code = main(["doctor", "--build", str(build), "--destination", str(target), *output_flag])
                    self.assertEqual(0, code)
                    if output_flag:
                        self.assertTrue(json.loads(output.getvalue())["ok"])
                    else:
                        self.assertIn("Vorabcheck", output.getvalue())
                        self.assertIn("Anmeldung", output.getvalue())
                    self.assertFalse(target.exists())

    def test_malformed_manifest_shapes_are_structured_failures(self) -> None:
        for manifest in ([], None, 42, "invalid", {"files": [None]}):
            with self.subTest(manifest=manifest), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                build = test_install.InstallTests().make_build(root)
                (build / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
                target = root / "new"
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(["doctor", "--build", str(build), "--destination", str(target), "--json"])
                self.assertEqual(2, code)
                report = json.loads(output.getvalue())
                failure = next(item for item in report["checks"] if item["code"] == "build-integrity")
                self.assertEqual("fail", failure["status"])
                self.assertTrue(failure["remedy"])
                self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
