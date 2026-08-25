from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from pos_boilerplate.cli import main
from pos_boilerplate.inventory import git_tracked_files, inventory
from pos_boilerplate.policy import ExportPolicy, PolicyError


class ExportPolicyTests(unittest.TestCase):
    def make_policy(self, root: Path, rules: list[dict[str, object]]) -> ExportPolicy:
        path = root / "policy.json"
        path.write_text(json.dumps({"schema_version": 1, "rules": rules}), encoding="utf-8")
        return ExportPolicy.load(path)

    def test_first_matching_rule_is_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            policy = self.make_policy(
                root,
                [
                    {
                        "id": "public-contracts",
                        "pattern": "system/contracts/**",
                        "action": "copy",
                        "reason": "Reusable system contracts",
                    },
                    {
                        "id": "remaining-system",
                        "pattern": "system/**",
                        "action": "exclude",
                        "reason": "Not reviewed yet",
                    },
                ],
            )

            classification = policy.classify("system/contracts/core/example.md")

            self.assertEqual(classification.rule_id, "public-contracts")
            self.assertEqual(classification.action, "copy")

    def test_unclassified_path_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            policy = self.make_policy(
                root,
                [
                    {
                        "id": "system-only",
                        "pattern": "system/**",
                        "action": "copy",
                        "reason": "System files",
                    }
                ],
            )

            with self.assertRaises(PolicyError):
                policy.classify("people/example.md")

    def test_invalid_action_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            with self.assertRaises(PolicyError):
                self.make_policy(
                    root,
                    [
                        {
                            "id": "invalid",
                            "pattern": "**",
                            "action": "publish-everything",
                            "reason": "Unsafe",
                        }
                    ],
                )

    def test_unsafe_target_and_module_are_rejected(self) -> None:
        with self.assertRaises(PolicyError):
            ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "escape",
                            "pattern": "**",
                            "action": "render",
                            "target": "../outside.md",
                            "reason": "unsafe",
                        }
                    ],
                }
            )
        with self.assertRaises(PolicyError):
            ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "escape",
                            "pattern": "**",
                            "action": "module",
                            "module": "../outside",
                            "reason": "unsafe",
                        }
                    ],
                }
            )


class InventoryTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)

    def test_git_inventory_uses_only_versioned_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.init_repo(root)
            (root / "system").mkdir()
            (root / "system" / "contract.md").write_text("contract", encoding="utf-8")
            (root / "private.md").write_text("tracked", encoding="utf-8")
            (root / "scratch.md").write_text("untracked", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "system/contract.md", "private.md"],
                check=True,
            )

            self.assertEqual(git_tracked_files(root), ["private.md", "system/contract.md"])

    def test_inventory_counts_actions_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            policy = ExportPolicy.from_data(
                {
                    "schema_version": 1,
                    "rules": [
                        {
                            "id": "core",
                            "pattern": "system/**",
                            "action": "copy",
                            "reason": "Reusable core",
                        },
                        {
                            "id": "private",
                            "pattern": "people/**",
                            "action": "exclude",
                            "reason": "Private instance data",
                        },
                    ],
                }
            )

            result = inventory(
                ["system/contracts/a.md", "people/example.md"],
                policy,
            )

            self.assertEqual(result.counts, {"copy": 1, "exclude": 1})
            self.assertEqual(result.unclassified, [])

            failing = inventory(["unknown/file.md"], policy)
            self.assertEqual(failing.unclassified, ["unknown/file.md"])

    def test_inventory_command_writes_report_and_fails_for_unknown_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            self.init_repo(source)
            (source / "known.md").write_text("known", encoding="utf-8")
            (source / "unknown.md").write_text("unknown", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "known.md", "unknown.md"], check=True)
            policy_path = root / "policy.json"
            policy_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "rules": [
                            {
                                "id": "known",
                                "pattern": "known.md",
                                "action": "copy",
                                "reason": "Known fixture",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = root / "report.json"

            exit_code = main(
                [
                    "inventory",
                    "--source",
                    str(source),
                    "--policy",
                    str(policy_path),
                    "--output",
                    str(report),
                ]
            )

            self.assertEqual(exit_code, 2)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["unclassified"], ["unknown.md"])


if __name__ == "__main__":
    unittest.main()
