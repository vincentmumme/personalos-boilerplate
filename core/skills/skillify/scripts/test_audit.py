#!/usr/bin/env python3
"""Tests for the SKILL.md envelope checks in audit.py."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("skillify_audit", Path(__file__).with_name("audit.py"))
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load skillify audit.py")

skillify_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = skillify_audit
SPEC.loader.exec_module(skillify_audit)


CURRENT = """---
name: demo-skill
description: "Use this for demo work."
metadata:
  pos_schema_version: pos-v1
  pos_id: 00000000-0000-7000-8000-000000000000
  pos_type: skill
  pos_title: "Skill: demo-skill"
  pos_created: "2026-11-01"
  pos_updated: "2026-11-01"
  pos_lifecycle: active
  pos_skill_version: 1.0.0
---

# Skill: demo-skill

## Purpose

Do the demo.
"""

LEGACY = """---
name: demo-skill
version: 1.0.0
description: "Use this for demo work."
triggers: ["demo"]
tools: ["shell"]
mutating: false
---

# Skill: demo-skill

## Contract
"""


class AuditEnvelopeTest(unittest.TestCase):
    def audit(self, text: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "demo-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(text, encoding="utf-8")
            result = skillify_audit.audit_skill(root, "demo-skill", run_global_check=False)
        return {item.name: item for item in result.items}

    def test_parse_metadata_reads_nested_pos_fields(self) -> None:
        meta = skillify_audit.parse_metadata(CURRENT)
        self.assertEqual("skill", meta["pos_type"])
        self.assertEqual("Skill: demo-skill", meta["pos_title"])

    def test_parse_metadata_handles_empty_and_block_lists(self) -> None:
        text = CURRENT.replace(
            "  pos_skill_version: 1.0.0\n",
            "  pos_skill_version: 1.0.0\n  pos_system_refs: []\n  pos_check_refs:\n    - \"[[system/checks/x]]\"\n",
        )
        meta = skillify_audit.parse_metadata(text)
        self.assertEqual("", meta["pos_system_refs"])
        self.assertEqual("[[system/checks/x]]", meta["pos_check_refs"])

    def test_current_envelope_passes(self) -> None:
        items = self.audit(CURRENT)
        self.assertEqual(skillify_audit.PASS, items["SKILL.md frontmatter"].status)
        self.assertEqual(skillify_audit.PASS, items["SKILL.md body"].status)
        self.assertEqual(skillify_audit.NA, items["Mutating guardrails"].status)

    def test_legacy_envelope_fails(self) -> None:
        items = self.audit(LEGACY)
        self.assertEqual(skillify_audit.FAIL, items["SKILL.md frontmatter"].status)
        self.assertIn("pos_id", items["SKILL.md frontmatter"].detail)

    def test_legacy_top_level_field_fails_next_to_current_envelope(self) -> None:
        text = CURRENT.replace("metadata:\n", "mutating: true\nmetadata:\n")
        items = self.audit(text)
        self.assertEqual(skillify_audit.FAIL, items["SKILL.md frontmatter"].status)
        self.assertIn("mutating", items["SKILL.md frontmatter"].detail)

    def test_unknown_top_level_field_fails(self) -> None:
        text = CURRENT.replace("metadata:\n", "foo: 1\nmetadata:\n")
        items = self.audit(text)
        self.assertEqual(skillify_audit.FAIL, items["SKILL.md frontmatter"].status)
        self.assertIn("unknown top-level fields: foo", items["SKILL.md frontmatter"].detail)

    def test_optional_top_level_fields_pass(self) -> None:
        text = CURRENT.replace("metadata:\n", "license: MIT\nallowed-tools: Read Grep\nmetadata:\n")
        items = self.audit(text)
        self.assertEqual(skillify_audit.PASS, items["SKILL.md frontmatter"].status)

    def test_body_without_h2_fails(self) -> None:
        items = self.audit(CURRENT.replace("## Purpose", "Purpose"))
        self.assertEqual(skillify_audit.FAIL, items["SKILL.md body"].status)

    def test_writes_require_check_refs(self) -> None:
        text = CURRENT.replace(
            "  pos_skill_version: 1.0.0\n",
            "  pos_skill_version: 1.0.0\n  pos_writes_profile_keys: [\"action\"]\n",
        )
        items = self.audit(text)
        self.assertEqual(skillify_audit.FAIL, items["SKILL.md frontmatter"].status)
        self.assertIn("pos_check_refs", items["SKILL.md frontmatter"].detail)

    def test_writes_enable_mutating_guardrails(self) -> None:
        text = CURRENT.replace(
            "  pos_skill_version: 1.0.0\n",
            "  pos_skill_version: 1.0.0\n"
            "  pos_writes_profile_keys: [\"action\"]\n"
            "  pos_check_refs: [\"[[system/checks/pos-v1-contract]]\"]\n",
        )
        items = self.audit(text)
        self.assertEqual(skillify_audit.PASS, items["SKILL.md frontmatter"].status)
        self.assertNotEqual(skillify_audit.NA, items["Mutating guardrails"].status)


if __name__ == "__main__":
    unittest.main()
