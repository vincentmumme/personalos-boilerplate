#!/usr/bin/env python3
"""Build or check the active PersonalOS skills manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = ROOT / "skills"
MANIFEST = SKILLS_ROOT / "manifest.json"
TIME_CONTEXT_SCRIPTS = ROOT / "system/data-model/scripts"
sys.path.insert(0, str(TIME_CONTEXT_SCRIPTS))
try:
    from time_context import resolve_timezone
finally:
    sys.path.pop(0)

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)


def scalar(body: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", body)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def collect() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    names: dict[str, str] = {}
    for path in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        relative = path.relative_to(SKILLS_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            raise SystemExit(f"Skill has no YAML frontmatter: {relative}")
        body = match.group("body")
        name = scalar(body, "name")
        lifecycle = scalar(body, "pos_lifecycle")
        if not name:
            raise SystemExit(f"Skill has no name: {relative}")
        if not lifecycle:
            raise SystemExit(f"Skill has no metadata.pos_lifecycle: {relative}")
        previous = names.get(name)
        if previous:
            raise SystemExit(f"Duplicate skill name {name}: {previous}, {relative}")
        names[name] = relative
        if lifecycle != "active":
            continue
        entries.append({"name": name, "path": relative})
    return sorted(entries, key=lambda item: item["name"])


def existing_payload() -> dict[str, Any]:
    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def build_payload(entries: list[dict[str, str]], generated_at: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_by": "personalos",
        "generated_at": generated_at,
        "selection": "metadata.pos_lifecycle == active",
        "skills": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    entries = collect()
    existing = existing_payload()
    structural_ok = (
        existing.get("schema_version") == 1
        and existing.get("generated_by") == "personalos"
        and existing.get("selection") == "metadata.pos_lifecycle == active"
        and existing.get("skills") == entries
    )
    if args.check:
        result = {
            "ok": structural_ok,
            "active_skills": len(entries),
            "manifest_skills": len(existing.get("skills") or []),
            "manifest": str(MANIFEST.relative_to(ROOT)),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if structural_ok else 1

    generated_at = str(existing.get("generated_at") or "") if structural_ok else datetime.now(tz=resolve_timezone(ROOT)).date().isoformat()
    payload = build_payload(entries, generated_at)
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "written", "active_skills": len(entries), "manifest": str(MANIFEST.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
