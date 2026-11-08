from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
REFERENCE = REPOSITORY / "reference"
AUDIT_SCRIPT = REPOSITORY / "core" / "skills" / "skillify" / "scripts" / "audit.py"


def _load(name: str, path: Path):
    # Unique module names: tests/test_audit.py already owns the name "test_audit".
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ShippedSkillEnvelopeTest(unittest.TestCase):
    """Every shipped skill must pass the Skillify envelope checks it is audited with."""

    def test_skill_local_audit_tests_pass(self) -> None:
        local = _load("skillify_audit_local_tests", AUDIT_SCRIPT.with_name("test_audit.py"))
        suite = unittest.defaultTestLoader.loadTestsFromModule(local)
        result = unittest.TestResult()
        suite.run(result)
        self.assertGreater(result.testsRun, 0)
        self.assertEqual([], [str(test) for test, _ in result.failures + result.errors])

    def test_shipped_skills_pass_envelope_checks(self) -> None:
        audit = _load("skillify_audit_shipped", AUDIT_SCRIPT)
        skills = sorted(path.parent for path in (REFERENCE / "skills").glob("*/SKILL.md"))
        self.assertTrue(skills)
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                result = audit.audit_skill(REFERENCE, skill_dir.name, run_global_check=False)
                items = {item.name: item for item in result.items}
                for name in ("SKILL.md frontmatter", "SKILL.md body"):
                    self.assertEqual(audit.PASS, items[name].status, f"{name}: {items[name].detail}")


if __name__ == "__main__":
    unittest.main()
