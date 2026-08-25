from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-resolvable.py")
ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("check_resolvable", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load check-resolvable.py")

check_resolvable = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_resolvable
SPEC.loader.exec_module(check_resolvable)


class CheckResolvableTests(unittest.TestCase):
    def test_current_resolver_preserves_idea_routing_boundaries(self) -> None:
        resolver = (ROOT / "skills" / "RESOLVER.md").read_text(encoding="utf-8")
        self.assertIn("Content-Ideen laufen ausschließlich über", resolver)
        self.assertIn("nur ungeklärter, aber erhaltenswerter Input wird als `capture`", resolver)
        self.assertIn("Ein möglicher späterer Projectgedanke bleibt Domain-Idea", resolver)

    def test_retired_skill_is_not_required_in_active_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skills" / "active-skill").mkdir(parents=True)
            (root / "skills" / "retired-skill").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "skills" / "active-skill" / "SKILL.md").write_text(
                "---\nname: active-skill\ndescription: An active test skill.\nstatus: active\n---\n",
                encoding="utf-8",
            )
            (root / "skills" / "retired-skill" / "SKILL.md").write_text(
                "---\nname: retired-skill\ndescription: A retired test skill.\n"
                "metadata:\n  pos_schema_version: pos-v1\n  pos_lifecycle: retired\n---\n",
                encoding="utf-8",
            )
            (root / "skills" / "retired-skill" / "routing-eval.jsonl").write_text(
                "this retired fixture is intentionally invalid json\n",
                encoding="utf-8",
            )
            (root / "skills" / "index.md").write_text(
                "[[skills/active-skill/SKILL]]\n",
                encoding="utf-8",
            )
            (root / "skills" / "RESOLVER.md").write_text(
                "| Trigger | Skill |\n|---|---|\n| active | [[skills/active-skill/SKILL]] |\n",
                encoding="utf-8",
            )

            findings, summary = check_resolvable.check(root)

            self.assertEqual([], findings)
            self.assertEqual(["active-skill"], summary["skills"])
            self.assertEqual(["retired-skill"], summary["retired_skills"])
            self.assertEqual(0, summary["routing_evals"])

    def test_active_skill_dependencies_and_write_interface_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = root / "skills" / "writer" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\nname: writer\ndescription: A sufficiently described writer skill.\n"
                "metadata:\n  pos_schema_version: pos-v1\n"
                "  pos_invokes_skill_refs: [\"[[skills/pos-verify/SKILL]]\"]\n---\n"
                "[[system/contracts/missing]] ../conventions/old.md\n",
                encoding="utf-8",
            )
            (root / "skills" / "index.md").write_text("[[skills/writer/SKILL]]\n")
            (root / "skills" / "RESOLVER.md").write_text("| writer | [[skills/writer/SKILL]] |\n")

            findings, _ = check_resolvable.check(root)
            codes = {finding.code for finding in findings}

            self.assertIn("legacy_skill_system_ref", codes)
            self.assertIn("skill_system_ref_missing", codes)
            self.assertIn("capability_write_interface_missing", codes)


if __name__ == "__main__":
    unittest.main()
