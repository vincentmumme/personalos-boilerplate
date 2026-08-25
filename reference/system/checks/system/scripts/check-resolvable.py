#!/usr/bin/env python3
"""
PersonalOS skill resolver health check.

Checks that every shared skill is visible in skills/index.md and reachable via
skills/RESOLVER.md, and flags simple resolver drift before it becomes invisible
agent behavior. Also rejects legacy LEARNINGS.md files in the skill layer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


SKILL_LINK_RE = re.compile(r"\[\[skills/([^/\]]+)/SKILL(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+/SKILL\.md)\)")
SYSTEM_LINK_RE = re.compile(r"\[\[(system/[^\]|#]+)")
NO_SKILL_EXPECTED = "__none__"
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
CONFLICT_SCAN_ROOTS = (
    "INDEX.md",
    "USER.md",
    "SOUL.md",
    "skills",
    "system",
)
CONFLICT_SCAN_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".sh"}


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None


@dataclass
class SkillInfo:
    slug: str
    path: str
    name: str | None
    description: str | None
    lifecycle: str


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    frontmatter: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter.append(line)

    i = 0
    while i < len(frontmatter):
        line = frontmatter[i]
        match = re.match(r"^(?:  )?([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, value = match.groups()
        value = value.strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block_lines: list[str] = []
            i += 1
            while i < len(frontmatter):
                next_line = frontmatter[i]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", next_line):
                    i -= 1
                    break
                block_lines.append(next_line.strip())
                i += 1
            value = " ".join(part for part in block_lines if part)
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        data[key] = value
        i += 1
    return data


def discover_skills(root: Path) -> dict[str, SkillInfo]:
    skills: dict[str, SkillInfo] = {}
    for skill_file in sorted((root / "skills").glob("*/SKILL.md")):
        slug = skill_file.parent.name
        fm = parse_frontmatter(skill_file)
        skills[slug] = SkillInfo(
            slug=slug,
            path=rel(skill_file, root),
            name=fm.get("name"),
            description=fm.get("description"),
            lifecycle=fm.get("pos_lifecycle") or fm.get("lifecycle") or fm.get("status") or "active",
        )
    return skills


def extract_skill_links(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    slugs = set(SKILL_LINK_RE.findall(text))
    for link in MARKDOWN_LINK_RE.findall(text):
        parts = Path(link).parts
        if len(parts) >= 2 and parts[-1] == "SKILL.md":
            slugs.add(parts[-2])
    return slugs


def pos_metadata_list(text: str, key: str) -> list[str]:
    match = re.search(rf"^  {re.escape(key)}:\s*(\[[^\n]*\])\s*$", text, re.M)
    if not match:
        return []
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def extract_resolver_rows(path: Path) -> list[tuple[str, str, str, int]]:
    rows: list[tuple[str, str, str, int]] = []
    if not path.exists():
        return rows

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|") or "skills/" not in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0].lower() in {"trigger", "---"}:
            continue
        rows.append((cells[0], stripped, line, lineno))
    return rows


def normalize_trigger(trigger: str) -> str:
    lowered = trigger.lower()
    lowered = re.sub(r"`[^`]+`", "", lowered)
    lowered = re.sub(r"\[\[[^\]]+\]\]", "", lowered)
    lowered = re.sub(r"[^a-z0-9äöüß]+", " ", lowered)
    return " ".join(lowered.split())


def load_routing_evals(root: Path, excluded_slugs: set[str] | None = None) -> list[tuple[str, Path, int, dict]]:
    fixtures: list[tuple[str, Path, int, dict]] = []
    excluded = excluded_slugs or set()
    for fixture in sorted((root / "skills").glob("*/routing-eval.jsonl")):
        slug = fixture.parent.name
        if slug in excluded:
            continue
        for lineno, line in enumerate(fixture.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                fixtures.append((slug, fixture, lineno, {"_error": str(exc)}))
                continue
            fixtures.append((slug, fixture, lineno, item))
    return fixtures


def iter_conflict_scan_files(root: Path) -> Iterable[Path]:
    for item in CONFLICT_SCAN_ROOTS:
        path = root / item
        if path.is_file() and path.suffix in CONFLICT_SCAN_SUFFIXES:
            yield path
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix in CONFLICT_SCAN_SUFFIXES:
                    yield child


def find_conflict_markers(root: Path) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in iter_conflict_scan_files(root):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if stripped.startswith(CONFLICT_MARKERS):
                marker = stripped.split(maxsplit=1)[0]
                findings.append((path, lineno, marker))
    return findings


def check(root: Path) -> tuple[list[Finding], dict]:
    findings: list[Finding] = []
    skills_dir = root / "skills"
    resolver_path = skills_dir / "RESOLVER.md"
    index_path = skills_dir / "index.md"
    discovered_skills = discover_skills(root)
    retired_skills = {slug for slug, info in discovered_skills.items() if info.lifecycle == "retired"}
    skills = {
        slug: info for slug, info in discovered_skills.items() if info.lifecycle != "retired"
    }

    if not skills_dir.exists():
        findings.append(Finding("error", "missing_skills_dir", "skills/ directory is missing", "skills"))
        return findings, {"skills": [], "resolver_rows": 0, "routing_evals": 0}

    if not resolver_path.exists():
        findings.append(Finding("error", "missing_resolver", "skills/RESOLVER.md is missing", "skills/RESOLVER.md"))
    if not index_path.exists():
        findings.append(Finding("error", "missing_index", "skills/index.md is missing", "skills/index.md"))

    for path, lineno, marker in find_conflict_markers(root):
        findings.append(
            Finding(
                "error",
                "conflict_marker",
                f"Merge conflict marker found: {marker}",
                f"{rel(path, root)}:{lineno}",
            )
        )

    for learnings_file in sorted(skills_dir.glob("*/LEARNINGS.md")):
        findings.append(
            Finding(
                "error",
                "legacy_learnings_file",
                "LEARNINGS.md is no longer used in PersonalOS skills; codify changes directly in SKILL.md, references, scripts, or rules",
                rel(learnings_file, root),
            )
        )

    index_links = extract_skill_links(index_path)
    resolver_links = extract_skill_links(resolver_path)
    skill_slugs = set(skills)

    for slug in sorted(skill_slugs - index_links):
        findings.append(
            Finding("error", "index_missing_skill", f"Skill is not listed in skills/index.md: {slug}", skills[slug].path)
        )
    for slug in sorted(index_links - skill_slugs):
        findings.append(
            Finding("error", "index_dead_skill_link", f"skills/index.md links to missing skill: {slug}", "skills/index.md")
        )

    for slug in sorted(skill_slugs - resolver_links):
        findings.append(
            Finding("error", "resolver_missing_skill", f"Skill is not reachable from skills/RESOLVER.md: {slug}", skills[slug].path)
        )
    for slug in sorted(resolver_links - skill_slugs):
        findings.append(
            Finding("error", "resolver_dead_skill_link", f"skills/RESOLVER.md links to missing skill: {slug}", "skills/RESOLVER.md")
        )

    names: dict[str, list[str]] = {}
    for slug, info in skills.items():
        skill_path = root / info.path
        skill_text = skill_path.read_text(encoding="utf-8")
        if "../conventions/" in skill_text or "skills/conventions/" in skill_text:
            findings.append(
                Finding(
                    "error",
                    "legacy_skill_system_ref",
                    f"Active skill still references retired skills/conventions: {slug}",
                    info.path,
                )
            )
        for target in sorted(set(SYSTEM_LINK_RE.findall(skill_text))):
            candidate = root / target
            if not candidate.is_file() and not candidate.with_suffix(".md").is_file():
                findings.append(
                    Finding(
                        "error",
                        "skill_system_ref_missing",
                        f"Active skill references missing system dependency: {target}",
                        info.path,
                    )
                )
        if "pos_schema_version: pos-v1" in skill_text:
            writes = pos_metadata_list(skill_text, "pos_writes_profile_keys")
            checks = pos_metadata_list(skill_text, "pos_check_refs")
            invokes = pos_metadata_list(skill_text, "pos_invokes_skill_refs")
            invokes_verifier = any("skills/pos-verify/SKILL" in item for item in invokes)
            if slug != "pos-verify" and invokes_verifier and not writes:
                findings.append(
                    Finding(
                        "error",
                        "capability_write_interface_missing",
                        f"POS-integrated skill invokes pos-verify but declares no pos_writes_profile_keys: {slug}",
                        info.path,
                    )
                )
            if writes and not checks:
                findings.append(
                    Finding(
                        "error",
                        "capability_check_interface_missing",
                        f"POS-writing skill declares no pos_check_refs: {slug}",
                        info.path,
                    )
                )
        if not info.name:
            findings.append(Finding("error", "missing_name", f"Skill frontmatter missing name: {slug}", info.path))
        else:
            names.setdefault(info.name, []).append(slug)
            if info.name != slug:
                findings.append(
                    Finding(
                        "warning",
                        "name_slug_mismatch",
                        f"Skill name differs from folder slug: name={info.name}, slug={slug}",
                        info.path,
                    )
                )
        if not info.description:
            findings.append(Finding("error", "missing_description", f"Skill frontmatter missing description: {slug}", info.path))
        elif len(info.description.strip()) < 20:
            findings.append(Finding("warning", "short_description", f"Skill description is very short: {slug}", info.path))

    for name, slugs in sorted(names.items()):
        if len(slugs) > 1:
            findings.append(
                Finding("error", "duplicate_skill_name", f"Multiple skill folders share name '{name}': {', '.join(slugs)}")
            )

    resolver_rows = extract_resolver_rows(resolver_path)
    row_triggers: dict[str, list[int]] = {}
    for trigger, stripped, raw_line, lineno in resolver_rows:
        row_links = set(SKILL_LINK_RE.findall(raw_line))
        if not row_links:
            findings.append(
                Finding("warning", "resolver_row_without_skill_link", f"Resolver row has no skill link: {trigger}", f"skills/RESOLVER.md:{lineno}")
            )
        normalized = normalize_trigger(trigger)
        if normalized:
            row_triggers.setdefault(normalized, []).append(lineno)

    for normalized, lines in sorted(row_triggers.items()):
        if len(lines) > 1:
            findings.append(
                Finding(
                    "warning",
                    "duplicate_trigger_text",
                    f"Resolver has duplicate or near-duplicate trigger text at lines {', '.join(map(str, lines))}: {normalized}",
                    "skills/RESOLVER.md",
                )
            )

    routing_evals = load_routing_evals(root, retired_skills)
    conflict_markers = find_conflict_markers(root)
    for slug, fixture, lineno, item in routing_evals:
        fixture_path = f"{rel(fixture, root)}:{lineno}"
        if "_error" in item:
            findings.append(Finding("error", "routing_eval_invalid_json", f"Invalid routing eval JSON: {item['_error']}", fixture_path))
            continue
        intent = item.get("intent")
        expected = item.get("expected_skill")
        if not intent or not isinstance(intent, str):
            findings.append(Finding("error", "routing_eval_missing_intent", "Routing eval missing string 'intent'", fixture_path))
        # Some upstream routing-eval formats use expected_skill: null for
        # negative fixtures. PersonalOS historically used "__none__"; accept
        # both so the local resolver guard stays compatible with upstream.
        if expected is None or expected == NO_SKILL_EXPECTED:
            continue
        if not expected or not isinstance(expected, str):
            findings.append(Finding("error", "routing_eval_missing_expected_skill", "Routing eval missing string/null 'expected_skill'", fixture_path))
            continue
        if expected not in skill_slugs:
            findings.append(Finding("error", "routing_eval_unknown_skill", f"Routing eval expects missing skill: {expected}", fixture_path))
        if expected != slug:
            findings.append(
                Finding(
                    "warning",
                    "routing_eval_cross_skill",
                    f"Routing eval under {slug} expects {expected}; keep cross-skill fixtures intentional",
                    fixture_path,
                )
            )
        if expected not in resolver_links:
            findings.append(
                Finding("error", "routing_eval_unreachable_skill", f"Routing eval expects skill not linked in resolver: {expected}", fixture_path)
            )

    summary = {
        "skills": sorted(skill_slugs),
        "retired_skills": sorted(retired_skills),
        "index_links": sorted(index_links),
        "resolver_links": sorted(resolver_links),
        "resolver_rows": len(resolver_rows),
        "routing_evals": len(routing_evals),
        "conflict_markers": len(conflict_markers),
        "errors": sum(1 for finding in findings if finding.level == "error"),
        "warnings": sum(1 for finding in findings if finding.level == "warning"),
    }
    return findings, summary


def print_text(findings: Iterable[Finding], summary: dict, strict: bool) -> None:
    print("PersonalOS check-resolvable")
    print(f"skills: {len(summary['skills'])}")
    print(f"retired skills: {len(summary.get('retired_skills', []))}")
    print(f"resolver rows: {summary['resolver_rows']}")
    print(f"routing evals: {summary['routing_evals']}")
    print(f"conflict markers: {summary['conflict_markers']}")
    print(f"errors: {summary['errors']}")
    print(f"warnings: {summary['warnings']}")
    print(f"strict: {str(strict).lower()}")
    print()

    findings = list(findings)
    if not findings:
        print("OK: all shared skills are indexed and resolver-reachable.")
        return

    for finding in findings:
        location = f" [{finding.path}]" if finding.path else ""
        print(f"{finding.level.upper()} {finding.code}: {finding.message}{location}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check PersonalOS skill resolver health.")
    parser.add_argument("--root", default=".", help="PersonalOS root path. Defaults to current directory.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failing.")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    findings, summary = check(root)

    if args.json:
        print(json.dumps({"summary": summary, "findings": [asdict(f) for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print_text(findings, summary, args.strict)

    if summary["errors"]:
        return 1
    if args.strict and summary["warnings"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
