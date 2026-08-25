from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .audit import audit_build
from .demo import DemoConfig, build_demo
from .install import InstallConfig, install_personalos
from .inventory import git_tracked_files, inventory
from .policy import ExportPolicy
from .secrets import effective_private_markers, scan_repository
from .sync import SyncConfig, sync_repository


def _load_string_list(path: Path | None, label: str) -> list[str]:
    if path is None:
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a JSON list of strings")
    return value


def _load_string_map(
    path: Path,
    label: str,
    *,
    error_message: str | None = None,
) -> dict[str, str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise ValueError(error_message or f"{label} must be a JSON object of string pairs")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pos-boilerplate",
        description="Build and verify the PersonalOS boilerplate.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory_parser = subparsers.add_parser(
        "inventory",
        help="Classify every versioned file in a PersonalOS source repository.",
    )
    inventory_parser.add_argument("--source", type=Path, required=True)
    inventory_parser.add_argument("--policy", type=Path, required=True)
    inventory_parser.add_argument("--output", type=Path, required=True)
    sync_parser = subparsers.add_parser(
        "sync",
        help="Build a privacy-checked boilerplate tree from a committed source revision.",
    )
    sync_parser.add_argument("--source", type=Path, required=True)
    sync_parser.add_argument("--policy", type=Path, required=True)
    sync_parser.add_argument("--output", type=Path, required=True)
    sync_parser.add_argument("--blueprints", type=Path)
    sync_parser.add_argument(
        "--replacements",
        type=Path,
        action="append",
        required=True,
        help="JSON replacement map; may be repeated and later maps override earlier ones.",
    )
    sync_parser.add_argument("--private-markers", type=Path, required=True)
    sync_parser.add_argument(
        "--public-safe-terms",
        type=Path,
        help="JSON list of public product terms that may also occur in private marker lists.",
    )
    audit_parser = subparsers.add_parser(
        "audit",
        help="Verify manifest integrity, privacy markers, module collisions and internal links.",
    )
    audit_parser.add_argument("--build", type=Path, required=True)
    audit_parser.add_argument(
        "--private-markers",
        type=Path,
        help="Optional local JSON marker list for release-grade privacy checks.",
    )
    audit_parser.add_argument("--public-safe-terms", type=Path)
    install_parser = subparsers.add_parser(
        "install",
        help="Install a clean PersonalOS from a verified boilerplate build.",
    )
    install_parser.add_argument("--build", type=Path, required=True)
    install_parser.add_argument("--destination", type=Path, required=True)
    module_group = install_parser.add_mutually_exclusive_group()
    module_group.add_argument("--module", action="append", default=[])
    module_group.add_argument(
        "--all-modules",
        action="store_true",
        help="Install the complete reference shape with every optional module.",
    )
    install_parser.add_argument("--values", type=Path, required=True)
    demo_parser = subparsers.add_parser(
        "demo",
        help=(
            "Erstellt aus der Boilerplate und sicheren Beispieldaten "
            "ein vollständiges PersonalOS für Aufnahmen."
        ),
    )
    demo_parser.add_argument("--build", type=Path, required=True)
    demo_parser.add_argument("--destination", type=Path, required=True)
    demo_parser.add_argument("--values", type=Path, required=True)
    demo_parser.add_argument("--fixtures", type=Path, required=True)
    secret_parser = subparsers.add_parser(
        "secret-scan",
        help="Scan tracked files and optional Git history without printing secret values.",
    )
    secret_parser.add_argument("--repository", type=Path, required=True)
    secret_parser.add_argument(
        "--history",
        action="store_true",
        help="Scan every historical Git blob in addition to the current worktree.",
    )
    secret_parser.add_argument("--private-markers", type=Path)
    secret_parser.add_argument("--public-safe-terms", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "inventory":
        policy = ExportPolicy.load(args.policy)
        result = inventory(git_tracked_files(args.source), policy)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary = ", ".join(f"{action}: {count}" for action, count in result.counts.items())
        print(summary or "No classified files")
        if result.unclassified:
            print(
                f"Unclassified source files: {len(result.unclassified)}. See {args.output}",
                file=sys.stderr,
            )
            return 2
        return 0
    if args.command == "sync":
        replacements: dict[str, str] = {}
        for replacement_path in args.replacements:
            replacement_map = json.loads(replacement_path.read_text(encoding="utf-8"))
            if not isinstance(replacement_map, dict) or not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in replacement_map.items()
            ):
                raise ValueError(
                    f"Replacements must be a JSON object of string pairs: {replacement_path}"
                )
            replacements.update(replacement_map)
        markers = _load_string_list(args.private_markers, "Private markers")
        public_safe_terms = _load_string_list(args.public_safe_terms, "Public safe terms")
        result = sync_repository(
            SyncConfig(
                source=args.source,
                output=args.output,
                policy=ExportPolicy.load(args.policy),
                replacements=replacements,
                private_markers=markers,
                blueprints=args.blueprints,
                public_safe_terms=tuple(public_safe_terms),
            )
        )
        print(
            f"Built {len(result.managed_files)} managed files from {result.source_revision[:12]}"
        )
        return 0
    if args.command == "audit":
        markers = _load_string_list(args.private_markers, "Private markers")
        public_safe_terms = _load_string_list(args.public_safe_terms, "Public safe terms")
        if args.private_markers is not None and not effective_private_markers(
            markers, public_safe_terms
        ):
            print("Private marker scan has no effective rules.", file=sys.stderr)
            return 3
        if not markers:
            print(
                "Warning: private marker scan is disabled; running structural and integrity checks only.",
                file=sys.stderr,
            )
        result = audit_build(args.build, markers, tuple(public_safe_terms))
        if not result.ok:
            for finding in result.findings:
                print(f"{finding.code}\t{finding.path}\t{finding.detail}", file=sys.stderr)
            return 3
        print("Build audit passed")
        return 0
    if args.command == "install":
        values = _load_string_map(args.values, "Install values")
        result = install_personalos(
            InstallConfig(
                build_root=args.build,
                destination=args.destination,
                modules=None if args.all_modules else tuple(args.module),
                values=values,
            )
        )
        print(f"Installed {result.file_count} files at {result.destination}")
        return 0
    if args.command == "demo":
        values = _load_string_map(
            args.values,
            "Demo-Werte",
            error_message="Die Demo-Werte müssen ein JSON-Objekt aus Textpaaren sein",
        )
        result = build_demo(
            DemoConfig(
                build_root=args.build,
                destination=args.destination,
                values=values,
                fixtures=args.fixtures,
            )
        )
        print(f"Demo mit {result.file_count} Dateien unter {result.destination} erstellt")
        return 0
    if args.command == "secret-scan":
        markers = _load_string_list(args.private_markers, "Private markers")
        public_safe_terms = _load_string_list(args.public_safe_terms, "Public safe terms")
        if args.private_markers is not None and not effective_private_markers(
            markers, public_safe_terms
        ):
            print("Private marker scan has no effective rules.", file=sys.stderr)
            return 4
        result = scan_repository(
            args.repository,
            include_history=args.history,
            private_markers=markers,
            public_safe_terms=public_safe_terms,
        )
        if not result.ok:
            for finding in result.findings:
                print(finding.render(), file=sys.stderr)
            return 4
        scope = "worktree and history" if args.history else "worktree"
        print(f"Secret scan passed ({scope})")
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
