from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pos_boilerplate.policy import ExportPolicy
from pos_boilerplate.sync import (
    PrivacyError,
    SyncConfig,
    SyncError,
    UnsafeOutputError,
    sync_repository,
)


class SyncTests(unittest.TestCase):
    def init_source(self, root: Path, files: dict[str, str]) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        for relative_path, content in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)

    def policy(self) -> ExportPolicy:
        return ExportPolicy.from_data(
            {
                "schema_version": 1,
                "rules": [
                    {
                        "id": "copy",
                        "pattern": "system/**",
                        "action": "copy",
                        "reason": "Core",
                    },
                    {
                        "id": "render",
                        "pattern": "USER.md",
                        "action": "render",
                        "target": "core/USER.md",
                        "reason": "Neutralized",
                    },
                    {
                        "id": "module",
                        "pattern": "skills/**",
                        "action": "module",
                        "module": "skills",
                        "reason": "Optional",
                    },
                    {
                        "id": "exclude",
                        "pattern": "people/**",
                        "action": "exclude",
                        "reason": "Private",
                    },
                ],
            }
        )

    def test_sync_builds_core_modules_and_manifest_from_committed_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            self.init_source(
                source,
                {
                    "system/contract.md": "stable contract\n",
                    "USER.md": "Owner: Private Person\n",
                    "skills/example/SKILL.md": "Help Private Person\n",
                    "people/private.md": "secret\n",
                },
            )
            replacements = {"Private Person": "{{user_name}}"}

            result = sync_repository(
                SyncConfig(
                    source=source,
                    output=output,
                    policy=self.policy(),
                    replacements=replacements,
                    private_markers=["Private Person"],
                )
            )

            self.assertEqual((output / "core/system/contract.md").read_text(), "stable contract\n")
            self.assertEqual((output / "core/USER.md").read_text(), "Owner: {{user_name}}\n")
            self.assertEqual(
                (output / "modules/skills/payload/skills/example/SKILL.md").read_text(),
                "Help {{user_name}}\n",
            )
            self.assertFalse((output / "core/people/private.md").exists())
            self.assertEqual(
                (output / "reference/system/contract.md").read_text(),
                "stable contract\n",
            )
            self.assertEqual(
                (output / "reference/skills/example/SKILL.md").read_text(),
                "Help {{user_name}}\n",
            )
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_revision"], result.source_revision)
            self.assertEqual(manifest["counts"], {"copy": 1, "exclude": 1, "module": 1, "render": 1})
            self.assertEqual(manifest["boilerplate_version"], "0.1.0")
            self.assertEqual(len(manifest["managed_files"]), 7)

    def test_sync_refuses_to_replace_unmanaged_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("do not delete\n", encoding="utf-8")
            self.init_source(source, {"system/contract.md": "stable contract\n"})

            with self.assertRaises(UnsafeOutputError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=output,
                        policy=self.policy(),
                        replacements={},
                        private_markers=[],
                    )
                )
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "do not delete\n")

    def test_sync_refuses_git_repository_even_when_it_has_a_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "repository"
            source.mkdir()
            output.mkdir()
            self.init_source(source, {"system/contract.md": "stable contract\n"})
            subprocess.run(["git", "init", "-q", str(output)], check=True)
            (output / "manifest.json").write_text("{}\n", encoding="utf-8")
            sentinel = output / "keep.txt"
            sentinel.write_text("repository content\n", encoding="utf-8")

            with self.assertRaises(UnsafeOutputError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=output,
                        policy=self.policy(),
                        replacements={},
                        private_markers=[],
                    )
                )

            self.assertTrue((output / ".git").is_dir())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "repository content\n")

    def test_sync_replaces_only_a_previous_managed_build(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "first\n"})
            config = SyncConfig(
                source=source,
                output=output,
                policy=self.policy(),
                replacements={},
                private_markers=[],
            )
            sync_repository(config)
            (source / "system/contract.md").write_text("second\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "update"], check=True)

            sync_repository(config)

            self.assertEqual(
                (output / "core/system/contract.md").read_text(encoding="utf-8"),
                "second\n",
            )

    def test_sync_uses_blueprint_instead_of_private_render_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            blueprints = root / "blueprints"
            source.mkdir()
            blueprints.mkdir()
            self.init_source(source, {"USER.md": "Private Person\n"})
            (blueprints / "USER.md").write_text("# User\n{{user_name}}\n", encoding="utf-8")
            policy = ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "render",
                            "pattern": "USER.md",
                            "action": "render",
                            "target": "core/USER.md",
                            "reason": "Neutralized",
                        }
                    ],
                }
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=output,
                    policy=policy,
                    blueprints=blueprints,
                    replacements={},
                    private_markers=["Private Person"],
                )
            )

            self.assertEqual((output / "core/USER.md").read_text(), "# User\n{{user_name}}\n")

    def test_static_blueprints_add_files_that_do_not_exist_in_private_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            blueprints = root / "blueprints"
            source.mkdir()
            (blueprints / "_static/identity").mkdir(parents=True)
            self.init_source(source, {"system/contract.md": "contract\n"})
            (blueprints / "_static/identity/me.md").write_text(
                "# {{user_name}}\n",
                encoding="utf-8",
            )

            result = sync_repository(
                SyncConfig(
                    source=source,
                    output=output,
                    policy=self.policy(),
                    blueprints=blueprints,
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (output / "core/identity/me.md").read_text(),
                "# {{user_name}}\n",
            )
            self.assertIn("core/identity/me.md", result.managed_files)

    def test_sync_rejects_symlinked_blueprint_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            blueprints = root / "blueprints"
            outside = root / "outside"
            source.mkdir()
            blueprints.mkdir()
            outside.mkdir()
            (outside / "private.md").write_text("outside\n", encoding="utf-8")
            (blueprints / "_static").symlink_to(outside, target_is_directory=True)
            self.init_source(source, {"system/contract.md": "contract\n"})

            with self.assertRaises(SyncError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=output,
                        policy=self.policy(),
                        blueprints=blueprints,
                        replacements={},
                        private_markers=[],
                    )
                )

            self.assertFalse(output.exists())

    def test_render_removes_links_to_excluded_instance_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "USER.md": "See [[people/private|the person]] and [[system/contract]].\n",
                    "people/private.md": "secret\n",
                    "system/contract.md": "contract\n",
                },
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=self.policy(),
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (root / "output/core/USER.md").read_text(),
                "See the person and [[system/contract]].\n",
            )

    def test_render_keeps_frontmatter_relations_valid_when_private_target_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "USER.md": (
                        'evidence_refs: ["[[people/private]]"]\n'
                        'affected_owner_refs: ["[[people/private]]"]\n'
                        'project_ref: "[[people/private]]"\n'
                    ),
                    "people/private.md": "secret\n",
                },
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=self.policy(),
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (root / "output/core/USER.md").read_text(),
                'evidence_refs: ["[[decisions/{{install_year}}/'
                '{{install_date}}-adopt-personalos-foundation]]"]\n'
                'affected_owner_refs: ["[[system/index]]"]\n'
                'project_ref: "[[examples/project]]"\n',
            )

    def test_sync_uses_one_committed_revision_when_index_diverges(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "committed\n"})
            (source / "system/contract.md").write_text("staged\n", encoding="utf-8")
            (source / "unknown.md").write_text("staged addition\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=self.policy(),
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (root / "output/core/system/contract.md").read_text(),
                "committed\n",
            )

    def test_sync_refuses_output_nested_inside_private_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "stable\n"})

            with self.assertRaises(UnsafeOutputError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=source / "generated",
                        policy=self.policy(),
                        replacements={},
                        private_markers=[],
                    )
                )

    def test_forged_manifest_does_not_authorize_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            output.mkdir()
            self.init_source(source, {"system/contract.md": "stable\n"})
            (output / "manifest.json").write_text('{"schema_version": 1}\n')
            sentinel = output / "keep.txt"
            sentinel.write_text("mine\n")

            with self.assertRaises(UnsafeOutputError):
                sync_repository(
                    SyncConfig(source, output, self.policy(), {}, [])
                )

            self.assertEqual(sentinel.read_text(), "mine\n")

    def test_publish_failure_restores_previous_managed_build(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "first\n"})
            config = SyncConfig(source, output, self.policy(), {}, [])
            sync_repository(config)
            (source / "system/contract.md").write_text("second\n")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "second"], check=True)
            real_replace = __import__("os").replace
            calls = 0

            def fail_second_replace(src: Path, dst: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected publish failure")
                real_replace(src, dst)

            with mock.patch("pos_boilerplate.sync.os.replace", side_effect=fail_second_replace):
                with self.assertRaises(OSError):
                    sync_repository(config)

            self.assertEqual(
                (output / "core/system/contract.md").read_text(),
                "first\n",
            )

    def test_render_resolves_bare_obsidian_slug_before_excluding_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "USER.md": "See [[private]].\n",
                    "people/private.md": "secret\n",
                },
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=self.policy(),
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual((root / "output/core/USER.md").read_text(), "See private.\n")

    def test_render_removes_resource_bullet_for_excluded_sibling_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "skills/example/SKILL.md": (
                        "## Resources\n\n"
                        "- `scripts/core.py` — portable core.\n"
                        "- `scripts/host_wrapper.py` — host integration.\n"
                    ),
                    "skills/example/scripts/core.py": "print('core')\n",
                    "skills/example/scripts/host_wrapper.py": "print('host')\n",
                },
            )
            policy = ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "exclude-host",
                            "pattern": "skills/example/scripts/host_wrapper.py",
                            "action": "exclude",
                            "reason": "Host-specific",
                        },
                        {
                            "id": "render-skill",
                            "pattern": "skills/example/**",
                            "action": "render",
                            "reason": "Portable skill",
                        },
                    ],
                }
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=policy,
                    replacements={},
                    private_markers=[],
                )
            )

            skill = (root / "output/core/skills/example/SKILL.md").read_text()
            self.assertIn("`scripts/core.py`", skill)
            self.assertNotIn("host_wrapper.py", skill)
            self.assertFalse(
                (root / "output/core/skills/example/scripts/host_wrapper.py").exists()
            )

    def test_render_replaces_private_decision_history_with_public_adoption_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "USER.md": (
                        'decision_refs: ["[[decisions/2026/private-system-decision]]"]\n'
                    ),
                    "decisions/2026/private-system-decision.md": "private history\n",
                },
            )
            policy = ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "render",
                            "pattern": "USER.md",
                            "action": "render",
                            "reason": "Public record",
                        },
                        {
                            "id": "private-decisions",
                            "pattern": "decisions/**",
                            "action": "exclude",
                            "reason": "Private history",
                        },
                    ],
                }
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=policy,
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (root / "output/core/USER.md").read_text(),
                'decision_refs: ["[[decisions/{{install_year}}/'
                '{{install_date}}-adopt-personalos-foundation]]"]\n',
            )

    def test_module_removes_relative_links_to_excluded_run_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {
                    "skills/example/SKILL.md": "Read [[references/run-2026-01-01|the old run]].\n",
                    "skills/example/references/run-2026-01-01.md": "private evidence\n",
                },
            )
            policy = ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "run-evidence",
                            "pattern": "skills/**/references/*2026*.md",
                            "action": "exclude",
                            "reason": "Private run evidence",
                        },
                        {
                            "id": "skills",
                            "pattern": "skills/**",
                            "action": "module",
                            "module": "skills",
                            "reason": "Optional skills",
                        },
                    ],
                }
            )

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=policy,
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertEqual(
                (root / "output/modules/skills/payload/skills/example/SKILL.md").read_text(),
                "Read the old run.\n",
            )

    def test_sync_stops_when_private_marker_survives(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "Private Person\n"})

            with self.assertRaises(PrivacyError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=root / "output",
                        policy=self.policy(),
                        replacements={},
                        private_markers=["Private Person"],
                    )
                )
            self.assertFalse((root / "output").exists())

    def test_sync_allows_only_explicit_public_terms_from_marker_list(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(source, {"system/contract.md": "Hermes and Private Person\n"})

            with self.assertRaises(PrivacyError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=root / "blocked",
                        policy=self.policy(),
                        replacements={},
                        private_markers=["Hermes", "Private Person"],
                        public_safe_terms=("Hermes",),
                    )
                )

            (source / "system/contract.md").write_text("Hermes\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "public term"], check=True)
            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "allowed",
                    policy=self.policy(),
                    replacements={},
                    private_markers=["Hermes", "Private Person"],
                    public_safe_terms=("Hermes",),
                )
            )
            self.assertEqual((root / "allowed/core/system/contract.md").read_text(), "Hermes\n")

    def test_api_user_path_is_not_mistaken_for_a_macos_home_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(source, {"skills/example/SKILL.md": "GET /users/@me\n"})

            sync_repository(
                SyncConfig(
                    source=source,
                    output=root / "output",
                    policy=self.policy(),
                    replacements={},
                    private_markers=[],
                )
            )

            self.assertTrue(
                (root / "output/modules/skills/payload/skills/example/SKILL.md").is_file()
            )

    def test_absolute_macos_home_path_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {"system/contract.md": "Read /" + "Users/private-owner/private.md\n"},
            )

            with self.assertRaises(PrivacyError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=root / "output",
                        policy=self.policy(),
                        replacements={},
                        private_markers=[],
                    )
                )

    def test_bare_absolute_macos_home_path_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_source(
                source,
                {"system/contract.md": "Home /" + "Users/private-owner\n"},
            )

            with self.assertRaises(PrivacyError):
                sync_repository(
                    SyncConfig(
                        source=source,
                        output=root / "output",
                        policy=self.policy(),
                        replacements={},
                        private_markers=[],
                    )
                )


if __name__ == "__main__":
    unittest.main()
