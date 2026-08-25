#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


SPEC = importlib.util.spec_from_file_location("pos_verify_run", Path(__file__).with_name("run.py"))
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load pos-verify run.py")

pos_verify_run = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pos_verify_run
SPEC.loader.exec_module(pos_verify_run)


class PosVerifyRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, relative_path: str, text: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_explicit_files_define_write_scope(self) -> None:
        self.write("notes/example.md", "---\ntitle: Example\n---\n\nBody\n")

        files, findings = pos_verify_run.normalize_files(
            self.root,
            ["notes/example.md", "notes/missing.md"],
            None,
        )

        self.assertEqual(["notes/example.md"], [pos_verify_run.rel(path, self.root) for path in files])
        self.assertEqual(["missing_or_deleted_file"], [finding.code for finding in findings])

    def test_repo_root_uses_script_vault_outside_vault_cwd(self) -> None:
        vault = self.root / "vault"
        script = vault / "skills" / "pos-verify" / "scripts" / "run.py"
        script.parent.mkdir(parents=True)
        script.write_text("# fixture\n", encoding="utf-8")
        (vault / "INDEX.md").write_text("# Index\n", encoding="utf-8")

        with mock.patch.object(pos_verify_run.subprocess, "run") as git_probe:
            root = pos_verify_run.repo_root(script_path=script)

        self.assertEqual(vault.resolve(), root)
        git_probe.assert_not_called()

    def test_entity_files_warn_on_missing_current_structure(self) -> None:
        path = self.write("people/example.md", "---\ntitle: Example\n---\n\nBody\n")
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        codes = {finding.code for finding in findings}
        self.assertIn("missing_updated", codes)
        self.assertIn("missing_current_truth", codes)
        self.assertIn("missing_timeline", codes)

    def test_markdown_and_legacy_checks_have_separate_owners(self) -> None:
        path = self.write("people/example.md", "---\ntitle: Example\n---\n\nBody\n")
        text = path.read_text(encoding="utf-8")

        markdown_codes = {
            finding.code
            for finding in pos_verify_run.check_markdown_integrity(
                path,
                self.root,
                text,
                pos_verify_run.alias_index(self.root),
            )
        }
        legacy_codes = {
            finding.code
            for finding in pos_verify_run.check_legacy_markdown_compatibility(path, self.root, text)
        }

        self.assertNotIn("missing_current_truth", markdown_codes)
        self.assertIn("missing_current_truth", legacy_codes)

    def test_pos_v1_skill_skips_legacy_skill_shape(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\n"
            "name: example\n"
            "description: Example skill.\n"
            "metadata:\n"
            "  pos_schema_version: pos-v1\n"
            "  pos_id: 019fecaa-1257-7094-84fd-ace36e97a088\n"
            "  pos_type: skill\n"
            "---\n\n"
            "# Example\n",
        )

        findings = pos_verify_run.check_legacy_skill_compatibility(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
        )

        self.assertEqual([], findings)

    def test_legacy_mutating_skill_accepts_canonical_mutation_contract(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example.\nmutating: true\n---\n\n"
            "# Example\n\nUse [[system/contracts/core/personalos-mutation-contract]] and pos-verify.\n",
        )
        codes = {
            item.code
            for item in pos_verify_run.check_legacy_skill_compatibility(path, self.root, path.read_text())
        }
        self.assertNotIn("mutating_skill_missing_pos_loop", codes)

    def test_legacy_mutating_skill_accepts_canonical_mutation_runbook(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example.\nmutating: true\n---\n\n"
            "# Example\n\nUse [[system/runbooks/core/personalos-mutation]] and pos-verify.\n",
        )
        codes = {
            item.code
            for item in pos_verify_run.check_legacy_skill_compatibility(path, self.root, path.read_text())
        }
        self.assertNotIn("mutating_skill_missing_pos_loop", codes)

    def test_legacy_mutating_skill_warns_without_contract_and_postflight(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example.\nmutating: true\n---\n\n# Example\n",
        )
        codes = {
            item.code
            for item in pos_verify_run.check_legacy_skill_compatibility(path, self.root, path.read_text())
        }
        self.assertIn("mutating_skill_missing_pos_loop", codes)

    def test_legacy_skill_accepts_canonical_system_rule_dependency(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example.\n---\n\n"
            "# Example\n\nUse [[system/rules/core/example]].\n",
        )
        codes = {
            item.code
            for item in pos_verify_run.check_legacy_skill_compatibility(path, self.root, path.read_text())
        }
        self.assertNotIn("legacy_rule_reference", codes)

    def test_legacy_skill_warns_on_legacy_conventions_dependency(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example.\n---\n\n"
            "# Example\n\nUse [[skills/conventions/example]].\n",
        )
        codes = {
            item.code
            for item in pos_verify_run.check_legacy_skill_compatibility(path, self.root, path.read_text())
        }
        self.assertIn("legacy_rule_reference", codes)

    def test_pos_v1_contract_delegates_runtime_enveloped_skill(self) -> None:
        path = self.write(
            "skills/example/SKILL.md",
            "---\nname: example\ndescription: Example skill.\nmetadata:\n  pos_schema_version: pos-v1\n---\n",
        )
        self.write("system/data-model/scripts/pos_v1.py", "# runtime fixture\n")
        contract = mock.Mock()
        contract.validate_text.return_value = []

        with mock.patch.object(pos_verify_run, "load_pos_v1_contract", return_value=contract):
            findings = pos_verify_run.check_pos_v1_contract(
                path,
                self.root,
                path.read_text(encoding="utf-8"),
                {"name": "example", "description": "Example skill.", "metadata": ""},
            )

        self.assertEqual([], findings)
        contract.validate_text.assert_called_once()

    def test_load_pos_v1_contract_resolves_runtime_sibling_imports(self) -> None:
        runtime_dir = self.root / "system/data-model/scripts"
        self.write("system/data-model/scripts/fixture_runtime_helper.py", "VALUE = 42\n")
        runtime_path = self.write(
            "system/data-model/scripts/pos_v1.py",
            "from fixture_runtime_helper import VALUE\n\n"
            "class Contract:\n"
            "    def __init__(self, root):\n"
            "        self.root = root\n"
            "        self.value = VALUE\n",
        )

        self.assertNotIn(str(runtime_dir.resolve()), sys.path)
        try:
            contract = pos_verify_run.load_pos_v1_contract(self.root, runtime_path)
        finally:
            sys.modules.pop("fixture_runtime_helper", None)

        self.assertEqual(42, contract.value)
        self.assertNotIn(str(runtime_dir.resolve()), sys.path)

    def test_duplicate_id_check_recognizes_runtime_enveloped_skill(self) -> None:
        record_id = "019fecaa-1257-7094-84fd-ace36e97a088"
        first = self.write(
            "skills/first/SKILL.md",
            f"---\nname: first\ndescription: First.\nmetadata:\n  pos_schema_version: pos-v1\n  pos_id: {record_id}\n---\n",
        )
        self.write(
            "skills/second/SKILL.md",
            f"---\nname: second\ndescription: Second.\nmetadata:\n  pos_schema_version: pos-v1\n  pos_id: {record_id}\n---\n",
        )

        findings = pos_verify_run.check_pos_v1_duplicate_ids(self.root, [first])

        self.assertEqual(["pos_v1_duplicate_id"], [finding.code for finding in findings])

    def test_duplicate_pos_v1_ids_are_checked_in_one_global_pass(self) -> None:
        record_id = "019fecaa-1257-7094-84fd-ace36e97a088"
        first = self.write(
            "system/rules/first.md",
            f"---\nschema_version: pos-v1\nid: {record_id}\ntype: rule\n---\n",
        )
        self.write(
            "system/rules/second.md",
            f"---\nschema_version: pos-v1\nid: {record_id}\ntype: rule\n---\n",
        )

        findings = pos_verify_run.check_pos_v1_duplicate_ids(
            self.root,
            [first],
            {first: first.read_text(encoding="utf-8")},
        )

        self.assertEqual(["pos_v1_duplicate_id"], [finding.code for finding in findings])

    def test_duplicate_id_check_ignores_body_examples_and_accepts_quoted_frontmatter(self) -> None:
        record_id = "019fecaa-1257-7094-84fd-ace36e97a088"
        first = self.write(
            "system/rules/first.md",
            f"---\nschema_version: pos-v1\nid: {record_id}\ntype: rule\n---\n",
        )
        self.write(
            "system/rules/example.md",
            f"---\nschema_version: pos-v1\nid: 019fecaa-1257-7094-84fd-ace36e97a099\ntype: rule\n---\n\n"
            f"```yaml\nid: {record_id}\n```\n",
        )

        self.assertEqual([], pos_verify_run.check_pos_v1_duplicate_ids(self.root, [first]))

        self.write(
            "system/rules/quoted.md",
            f"---\nschema_version: pos-v1\nid: '{record_id}'\ntype: rule\n---\n",
        )
        findings = pos_verify_run.check_pos_v1_duplicate_ids(self.root, [first])

        self.assertEqual(["pos_v1_duplicate_id"], [finding.code for finding in findings])

    def test_pos_v1_contract_delegates_text_and_converts_findings(self) -> None:
        path = self.write("system/rules/example.md", "---\nschema_version: pos-v1\ntype: rule\n---\n")
        self.write("system/data-model/scripts/pos_v1.py", "# runtime fixture\n")
        contract = mock.Mock()
        contract.validate_text.return_value = [
            SimpleNamespace(level="fail", code="example", path="system/rules/example.md", message="bad", remediation="fix")
        ]

        with mock.patch.object(pos_verify_run, "load_pos_v1_contract", return_value=contract):
            findings = pos_verify_run.check_pos_v1_contract(
                path,
                self.root,
                path.read_text(encoding="utf-8"),
                {"schema_version": "pos-v1"},
            )

        contract.validate_text.assert_called_once_with(
            path.read_text(encoding="utf-8"),
            "system/rules/example.md",
        )
        self.assertEqual(["example"], [finding.code for finding in findings])

    def test_pos_v1_contract_reports_missing_and_failed_runtime(self) -> None:
        path = self.write("system/rules/example.md", "---\nschema_version: pos-v1\ntype: rule\n---\n")
        text = path.read_text(encoding="utf-8")
        missing = pos_verify_run.check_pos_v1_contract(path, self.root, text, {"schema_version": "pos-v1"})
        self.assertEqual(["pos_v1_runtime_missing"], [finding.code for finding in missing])

        self.write("system/data-model/scripts/pos_v1.py", "# runtime fixture\n")
        with mock.patch.object(pos_verify_run, "load_pos_v1_contract", side_effect=RuntimeError("broken")):
            failed = pos_verify_run.check_pos_v1_contract(path, self.root, text, {"schema_version": "pos-v1"})
        self.assertEqual(["pos_v1_registry_error"], [finding.code for finding in failed])

    def test_generated_artifact_check_handles_skip_drift_and_runtime_failure(self) -> None:
        ordinary = self.write("system/rules/example.md", "# Example\n")
        self.assertEqual([], pos_verify_run.check_pos_v1_generated_if_needed(self.root, [ordinary]))

        registry = self.write("system/data-model/registry.yaml", "version: 1\n")
        missing = pos_verify_run.check_pos_v1_generated_if_needed(self.root, [registry])
        self.assertEqual(["pos_v1_runtime_missing"], [finding.code for finding in missing])

        self.write("system/data-model/scripts/pos_v1.py", "# runtime fixture\n")
        contract = mock.Mock()
        contract.build_generated.return_value = ["system/data-model/generated/manifest.json"]
        with mock.patch.object(pos_verify_run, "load_pos_v1_contract", return_value=contract):
            drift = pos_verify_run.check_pos_v1_generated_if_needed(self.root, [registry])
        self.assertEqual(["pos_v1_generated_drift"], [finding.code for finding in drift])
        contract.build_generated.assert_called_once_with(check=True)

        with mock.patch.object(pos_verify_run, "load_pos_v1_contract", side_effect=RuntimeError("broken")):
            failed = pos_verify_run.check_pos_v1_generated_if_needed(self.root, [registry])
        self.assertEqual(["pos_v1_generated_drift"], [finding.code for finding in failed])

    def test_conventions_do_not_require_frontmatter(self) -> None:
        path = self.write("skills/conventions/example.md", "# Convention\n\nBody\n")
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        self.assertNotIn("missing_frontmatter", {finding.code for finding in findings})

    def test_table_escaped_wikilink_pipe_resolves_target(self) -> None:
        self.write("skills/example/SKILL.md", "---\nname: example\n---\n")
        path = self.write("system/observability/cron-jobs.md", "| Skill |\n|---|\n| [[skills/example/SKILL\\|example]] |\n")
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        self.assertNotIn("broken_wikilink", {finding.code for finding in findings})

    def test_record_and_same_stem_companion_directory_are_not_ambiguous(self) -> None:
        self.write("business/brands/example.md", "---\ntitle: Example\n---\n")
        self.write("business/brands/example/tone-of-voice.md", "---\ntitle: Voice\n---\n")
        path = self.write("business/brands/index.md", "[[business/brands/example]]\n")

        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
            strict_links=True,
        )

        self.assertNotIn("ambiguous_wikilink", {finding.code for finding in findings})

    def test_genuine_multi_file_wikilink_ambiguity_is_still_reported(self) -> None:
        self.write("one/example.md", "---\ntitle: One\n---\n")
        self.write("two/example.md", "---\ntitle: Two\n---\n")
        path = self.write("index.md", "[[example]]\n")
        findings = pos_verify_run.check_markdown_integrity(
            path, self.root, path.read_text(), pos_verify_run.alias_index(self.root), strict_links=True
        )
        self.assertIn("ambiguous_wikilink", {finding.code for finding in findings})

    def test_directory_only_wikilink_target_is_broken(self) -> None:
        (self.root / "system/only-directory").mkdir(parents=True)
        path = self.write("index.md", "[[system/only-directory]]\n")
        findings = pos_verify_run.check_markdown_integrity(
            path, self.root, path.read_text(), pos_verify_run.alias_index(self.root), strict_links=True
        )
        self.assertIn("broken_wikilink", {finding.code for finding in findings})

    def test_pos_v1_internal_markdown_links_are_rejected_outside_portable_skills(self) -> None:
        record = self.write(
            "projects/example/example.md",
            "---\nschema_version: pos-v1\ntype: project\n---\n"
            "[Legacy](../other.md) [Web](https://example.com) ` [Code](../code.md) `\n"
            "```markdown\n[Fenced](../fenced.md)\n```\n",
        )
        skill = self.write(
            "skills/example/SKILL.md",
            "---\nschema_version: pos-v1\ntype: skill\n---\n[Resource](references/example.md)\n",
        )

        record_findings = pos_verify_run.check_markdown_integrity(
            record, self.root, record.read_text(), pos_verify_run.alias_index(self.root)
        )
        skill_findings = pos_verify_run.check_markdown_integrity(
            skill, self.root, skill.read_text(), pos_verify_run.alias_index(self.root)
        )

        self.assertEqual(
            ["pos_v1_internal_markdown_link"],
            [finding.code for finding in record_findings if finding.code == "pos_v1_internal_markdown_link"],
        )
        self.assertNotIn("pos_v1_internal_markdown_link", {finding.code for finding in skill_findings})

    def test_canonical_automation_output_profile_passes(self) -> None:
        path = self.write(
            "automations/example/outputs/2026-07-10.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: source\n"
            "pos_domain: automations\n"
            "subtype: automation-output\n"
            "role: automation-output\n"
            "status: success\n"
            "title: 'Example: 2026-07-10'\n"
            "automation: example\n"
            "run_date: 2026-07-10T17:30:00+02:00\n"
            "run_status: success\n"
            "run_trigger: manual\n"
            "briefing_include: false\n"
            "briefing_section: system\n"
            "summary: Example completed.\n"
            "priority: low\n"
            "updated: 2026-07-10\n"
            "tags: []\n"
            "---\n\n"
            "# Example\n\n## Summary\nComplete.\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        profile_codes = {finding.code for finding in findings if finding.code.startswith("v1_")}
        self.assertEqual(set(), profile_codes)

    def test_v1_legacy_automation_type_fails(self) -> None:
        path = self.write(
            "automations/example/outputs/legacy.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: automation-output\n"
            "pos_domain: automations\n"
            "role: automation-output\n"
            "status: success\n"
            "title: Legacy\n"
            "updated: 2026-07-10\n"
            "tags: []\n"
            "---\n\n# Legacy\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        self.assertIn("v1_automation_output_type", {finding.code for finding in findings})

    def test_explicit_source_run_report_under_system_runs_uses_source_profile(self) -> None:
        path = self.write(
            "interactions/conversations/gmail/_system/runs/scan-example.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: source\n"
            "pos_domain: interactions\n"
            "role: run-report\n"
            "status: active\n"
            "title: Gmail Context Run\n"
            "source_kind: email-scan\n"
            "source: gws\n"
            "updated: 2026-07-12\n"
            "tags: []\n"
            "---\n\n"
            "# Gmail Context Run\n\n## Summary\nCompleted.\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )

        profile_codes = {finding.code for finding in findings if finding.code.startswith("v1_")}
        self.assertEqual(set(), profile_codes)

    def test_project_quality_budgets_warn_on_bloat_and_shadow_tasks(self) -> None:
        long_truth = " ".join(["word"] * 401)
        state = "\n".join(f"- state {i}" for i in range(13))
        threads = "\n".join(f"- thread {i}" for i in range(10)) + "\n- [ ] hidden project task"
        path = self.write(
            "projects/example.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: project\n"
            "pos_domain: projects\n"
            "role: canonical-record\n"
            "status: active\n"
            "title: Example\n"
            "updated: 2026-07-10\n"
            "tags: []\n"
            "---\n\n"
            "# Example\n\n"
            f"## Current Truth\n{long_truth}\n\n"
            f"## State\n{state}\n\n"
            "## Scope Boundary\nScope.\n\n"
            "## Repo / External Truth\nRepo.\n\n"
            "## Stakeholders\nStakeholders.\n\n"
            "## Decisions\nDecisions.\n\n"
            f"## Open Threads\n{threads}\n\n"
            "## See Also\nNone.\n\n"
            "---\n\n## Timeline\n- **2026-07-10** | Created.\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )
        codes = {finding.code for finding in findings}
        self.assertIn("current_truth_overlong", codes)
        self.assertIn("state_too_many_bullets", codes)
        self.assertIn("open_threads_too_many_bullets", codes)
        self.assertIn("project_shadow_task_list", codes)

    def test_person_quality_budgets_warn_on_interaction_diary_bloat(self) -> None:
        long_truth = " ".join(["context"] * 501)
        state = "\n".join(f"- state {i}" for i in range(13))
        threads = "\n".join(f"- thread {i}" for i in range(11))
        path = self.write(
            "people/recurring-contact.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: person\n"
            "pos_domain: people\n"
            "role: canonical-record\n"
            "status: active\n"
            "title: Recurring Contact\n"
            "updated: 2026-07-28\n"
            "tags: []\n"
            "---\n\n"
            "# Recurring Contact\n\n"
            f"## Current Truth\n{long_truth}\n\n"
            f"## State\n{state}\n\n"
            "## Relationship\nActive collaborator.\n\n"
            f"## Open Threads\n{threads}\n\n"
            "## See Also\nNone.\n\n"
            "---\n\n## Timeline\n- **2026-07-28** | Created.\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )
        codes = {finding.code for finding in findings}
        self.assertIn("current_truth_overlong", codes)
        self.assertIn("state_too_many_bullets", codes)
        self.assertIn("open_threads_too_many_bullets", codes)

    def test_project_quality_budgets_accept_compact_project(self) -> None:
        path = self.write(
            "projects/compact.md",
            "---\n"
            "schema_version: pos-gbrain-v1\n"
            "type: project\n"
            "pos_domain: projects\n"
            "role: canonical-record\n"
            "status: active\n"
            "title: Compact\n"
            "updated: 2026-07-10\n"
            "tags: []\n"
            "---\n\n"
            "# Compact\n\n"
            "## Current Truth\nShort present state.\n\n"
            "## State\n- active\n\n"
            "## Scope Boundary\nScope.\n\n"
            "## Repo / External Truth\nRepo.\n\n"
            "## Stakeholders\nStakeholders.\n\n"
            "## Decisions\nDecisions.\n\n"
            "## Open Threads\n- one outcome-level thread\n\n"
            "## See Also\nNone.\n\n"
            "---\n\n## Timeline\n- **2026-07-10** | Created.\n",
        )
        findings = pos_verify_run.check_markdown(
            path,
            self.root,
            path.read_text(encoding="utf-8"),
            pos_verify_run.alias_index(self.root),
        )
        quality_codes = {
            "current_truth_overlong",
            "state_too_many_bullets",
            "open_threads_too_many_bullets",
            "project_shadow_task_list",
        }
        self.assertTrue(quality_codes.isdisjoint({finding.code for finding in findings}))


if __name__ == "__main__":
    unittest.main()
