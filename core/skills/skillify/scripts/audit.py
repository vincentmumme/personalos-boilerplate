#!/usr/bin/env python3
"""
PersonalOS Skillify audit.

Audits whether a target skill is hardened enough to count as "skillified" in
the PersonalOS skill layer. This intentionally complements
system/checks/system/scripts/check-resolvable.py: check-resolvable verifies global routing health;
this script verifies one skill against the Skillify checklist.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


PASS = "pass"
FAIL = "fail"
WARN = "warn"
NA = "not_applicable"

REQUIRED_FRONTMATTER = ("name", "version", "description", "triggers", "tools", "mutating")
REQUIRED_SECTIONS = (
    "## Contract",
    "## Phases",
    "## Output Format",
    "## Anti-Patterns",
    "## Tools Used",
)

SCRIPT_HINTS = (
    "script",
    "deterministic",
    "parser",
    "parse",
    "api",
    "endpoint",
    "sync",
    "cron",
    "scan",
    "import",
    "export",
    "migration",
    "batch",
    "bulk",
)
EXTERNAL_OR_SIDE_EFFECT_HINTS = (
    "api",
    "endpoint",
    "external",
    "calendar",
    "email",
    "gmail",
    "whatsapp",
    "drive",
    "lexware",
    "tally",
    "webhook",
    "cron",
    "automation",
    "side effect",
    "file mutation",
)
LLM_HINTS = (
    "llm",
    "model",
    "synthesis",
    "judgment",
    "ranking",
    "critique",
    "writing quality",
    "extraction quality",
    "cross-model",
    "cross-modal",
)
BULK_HINTS = (
    "bulk",
    "batch",
    "migration",
    "archive",
    "scan",
    "import",
    "enrichment",
    "many items",
)


@dataclass
class AuditItem:
    name: str
    status: str
    detail: str


@dataclass
class AuditResult:
    target: str
    path: str
    ok: bool
    passed: int
    failed: int
    warnings: int
    not_applicable: int
    items: list[AuditItem]


def default_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str | list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter.append(line)

    data: dict[str, str | list[str]] = {}
    i = 0
    while i < len(frontmatter):
        line = frontmatter[i]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue

        key, raw_value = match.groups()
        value = raw_value.strip()

        if value in {"|", ">"}:
            block: list[str] = []
            i += 1
            while i < len(frontmatter):
                next_line = frontmatter[i]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", next_line):
                    i -= 1
                    break
                block.append(next_line.strip())
                i += 1
            data[key] = " ".join(part for part in block if part)
        elif not value:
            items: list[str] = []
            i += 1
            while i < len(frontmatter):
                next_line = frontmatter[i]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", next_line):
                    i -= 1
                    break
                item_match = re.match(r"^\s*-\s*(.*)$", next_line)
                if item_match:
                    item = item_match.group(1).strip()
                    if (item.startswith('"') and item.endswith('"')) or (
                        item.startswith("'") and item.endswith("'")
                    ):
                        item = item[1:-1]
                    items.append(item)
                i += 1
            data[key] = items
        else:
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            data[key] = value
        i += 1

    return data


def boolish(value: str | list[str] | None) -> bool:
    if isinstance(value, list):
        return bool(value)
    return str(value).strip().lower() == "true"


def is_missing_frontmatter_value(value: str | list[str] | None) -> bool:
    if value is None:
        return True
    if isinstance(value, list):
        return not any(item.strip() for item in value)
    return not str(value).strip()


def has_any(text: str, needles: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def find_skill_dir(root: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.name == "SKILL.md":
        return candidate.expanduser().resolve().parent
    if candidate.exists():
        path = candidate.expanduser().resolve()
        return path.parent if path.name == "SKILL.md" else path

    skill_dir = root / "skills" / target
    if skill_dir.exists():
        return skill_dir

    raise FileNotFoundError(f"Cannot resolve skill target: {target}")


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def test_files(root: Path) -> list[Path]:
    tests_dir = root / "tests"
    if not tests_dir.exists():
        return []
    return sorted(
        path
        for path in tests_dir.rglob("*")
        if path.is_file() and path.suffix in {".py", ".json", ".jsonl", ".md"}
    )


def skill_local_test_files(skill_dir: Path) -> list[Path]:
    paths: list[Path] = []
    tests_dir = skill_dir / "tests"
    if tests_dir.exists():
        paths.extend(
            path
            for path in tests_dir.rglob("*")
            if path.is_file() and path.suffix in {".py", ".json", ".jsonl", ".md"}
        )

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        paths.extend(
            path
            for path in scripts_dir.rglob("*.py")
            if path.is_file() and (path.name.startswith("test_") or path.name.endswith("_test.py"))
        )

    return sorted(set(paths))


def files_mention(paths: Iterable[Path], needles: Iterable[str]) -> bool:
    needle_list = [needle.lower() for needle in needles if needle]
    for path in paths:
        text = read_text(path).lower()
        if any(needle in text for needle in needle_list):
            return True
    return False


def routing_eval_stats(path: Path, slug: str) -> tuple[int, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return 0, ["routing-eval.jsonl is missing"]

    count = 0
    for lineno, line in enumerate(read_text(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON: {exc}")
            continue
        if item.get("expected_skill") != slug:
            errors.append(f"line {lineno}: expected_skill must be {slug}")
            continue
        if not isinstance(item.get("intent"), str) or not item["intent"].strip():
            errors.append(f"line {lineno}: missing non-empty intent")
            continue
        count += 1
    return count, errors


def run_check_resolvable(root: Path) -> tuple[bool, str]:
    script = root / "system" / "checks" / "system" / "scripts" / "check-resolvable.py"
    if not script.exists():
        return False, "system/checks/system/scripts/check-resolvable.py is missing"

    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        return True, "check-resolvable passed"
    output = completed.stdout.strip() or completed.stderr.strip()
    return False, output[:1000]


def audit_skill(root: Path, target: str, run_global_check: bool = True) -> AuditResult:
    root = root.expanduser().resolve()
    skill_dir = find_skill_dir(root, target)
    slug = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    items: list[AuditItem] = []

    if not skill_path.exists():
        items.append(AuditItem("SKILL.md", FAIL, f"{rel(skill_path, root)} is missing"))
        return build_result(slug, skill_path, items)

    text = read_text(skill_path)
    lower_text = text.lower()
    fm = parse_frontmatter(text)

    missing_fm = [key for key in REQUIRED_FRONTMATTER if is_missing_frontmatter_value(fm.get(key))]
    if missing_fm:
        items.append(AuditItem("SKILL.md frontmatter", FAIL, f"missing: {', '.join(missing_fm)}"))
    elif fm.get("name") != slug:
        items.append(AuditItem("SKILL.md frontmatter", FAIL, f"name={fm.get('name')} does not match slug={slug}"))
    else:
        items.append(AuditItem("SKILL.md frontmatter", PASS, "required fields present and name matches slug"))

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing_sections:
        items.append(AuditItem("SKILL.md body", FAIL, f"missing sections: {', '.join(missing_sections)}"))
    else:
        items.append(AuditItem("SKILL.md body", PASS, "required body sections present"))

    local_tests = skill_local_test_files(skill_dir)
    local_test_set = {path.resolve() for path in local_tests}
    script_files = sorted(
        path for path in (skill_dir / "scripts").rglob("*") if path.is_file()
        and path.resolve() not in local_test_set
    ) if (skill_dir / "scripts").exists() else []
    script_applicable = has_any(text, SCRIPT_HINTS)
    if script_files:
        items.append(AuditItem("Deterministic code", PASS, f"{len(script_files)} script file(s) found"))
    elif script_applicable:
        items.append(AuditItem("Deterministic code", WARN, "skill text suggests repeatable code may apply, but no scripts/ files exist"))
    else:
        items.append(AuditItem("Deterministic code", NA, "no deterministic code need detected"))

    tests = sorted(set(test_files(root) + local_tests))
    script_needles = [slug] + [path.name for path in script_files]
    if script_files:
        if files_mention(tests, script_needles):
            items.append(AuditItem("Unit tests", PASS, "tests mention the skill or script files"))
        else:
            items.append(AuditItem("Unit tests", FAIL, "deterministic scripts exist but no matching root or skill-local test mention was found"))
    else:
        items.append(AuditItem("Unit tests", NA, "no deterministic script files detected"))

    needs_integration = has_any(text, EXTERNAL_OR_SIDE_EFFECT_HINTS) or boolish(fm.get("mutating"))
    has_smoke = any(term in lower_text for term in ("e2e", "smoke", "integration test", "integration checks"))
    if needs_integration and has_smoke:
        items.append(AuditItem("Integration or E2E smoke", PASS, "skill documents integration or smoke verification"))
    elif needs_integration:
        items.append(AuditItem("Integration or E2E smoke", WARN, "side effects or external systems detected; document an integration or E2E smoke check"))
    else:
        items.append(AuditItem("Integration or E2E smoke", NA, "no external or mutating integration need detected"))

    needs_llm_eval = has_any(text, LLM_HINTS)
    has_quality_gate = any(term in lower_text for term in ("cross-model", "cross-modal", "llm eval", "quality review", "critique"))
    if needs_llm_eval and has_quality_gate:
        items.append(AuditItem("LLM quality eval", PASS, "quality review or cross-model gate is documented"))
    elif needs_llm_eval:
        items.append(AuditItem("LLM quality eval", WARN, "LLM-heavy behavior detected; document quality eval or waiver"))
    else:
        items.append(AuditItem("LLM quality eval", NA, "no LLM-heavy behavior detected"))

    resolver_text = read_text(root / "skills" / "RESOLVER.md") if (root / "skills" / "RESOLVER.md").exists() else ""
    if f"skills/{slug}/SKILL" in resolver_text:
        items.append(AuditItem("Resolver route", PASS, "resolver links to the skill"))
    else:
        items.append(AuditItem("Resolver route", FAIL, "skills/RESOLVER.md has no route to this skill"))

    index_text = read_text(root / "skills" / "index.md") if (root / "skills" / "index.md").exists() else ""
    if f"skills/{slug}/SKILL" in index_text:
        items.append(AuditItem("Index navigation", PASS, "skills/index.md lists the skill"))
    else:
        items.append(AuditItem("Index navigation", FAIL, "skills/index.md does not list the skill"))

    routing_count, routing_errors = routing_eval_stats(skill_dir / "routing-eval.jsonl", slug)
    if routing_count >= 3 and not routing_errors:
        items.append(AuditItem("Resolver eval", PASS, f"{routing_count} routing eval intents found"))
    else:
        detail = f"{routing_count} valid routing eval intents; " + "; ".join(routing_errors)
        items.append(AuditItem("Resolver eval", FAIL, detail.strip()))

    if run_global_check:
        ok, detail = run_check_resolvable(root)
        items.append(AuditItem("Check-resolvable", PASS if ok else FAIL, detail))
    else:
        items.append(AuditItem("Check-resolvable", WARN, "global check skipped by caller"))

    if boolish(fm.get("mutating")):
        guardrail_groups = {
            "provenance/source": ("provenance", "source", "source pointer"),
            "write boundaries": ("write target", "write targets", "write boundaries", "write paths", "canonical"),
            "failure handling": ("failure", "partial-write", "partial write", "partial"),
            "verification": ("verify", "verification", "test", "check"),
        }
        missing = [
            label for label, needles in guardrail_groups.items() if not has_any(text, needles)
        ]
        if missing:
            items.append(AuditItem("Mutating guardrails", FAIL, f"missing: {', '.join(missing)}"))
        else:
            items.append(AuditItem("Mutating guardrails", PASS, "provenance, write boundaries, failure handling, and verification are documented"))
    else:
        items.append(AuditItem("Mutating guardrails", NA, "skill is not mutating"))

    needs_bulk = has_any(text, BULK_HINTS)
    has_bulk_guard = any(term in lower_text for term in ("test-before-bulk", "small sample", "3-5", "probe"))
    if needs_bulk and has_bulk_guard:
        items.append(AuditItem("Test-before-bulk", PASS, "bulk safety gate is documented"))
    elif needs_bulk:
        items.append(AuditItem("Test-before-bulk", FAIL, "bulk/import/migration behavior detected without test-before-bulk guardrail"))
    else:
        items.append(AuditItem("Test-before-bulk", NA, "no bulk behavior detected"))

    return build_result(slug, skill_path, items)


def build_result(slug: str, skill_path: Path, items: list[AuditItem]) -> AuditResult:
    failed = sum(1 for item in items if item.status == FAIL)
    warnings = sum(1 for item in items if item.status == WARN)
    passed = sum(1 for item in items if item.status == PASS)
    not_applicable = sum(1 for item in items if item.status == NA)
    return AuditResult(
        target=slug,
        path=str(skill_path),
        ok=failed == 0,
        passed=passed,
        failed=failed,
        warnings=warnings,
        not_applicable=not_applicable,
        items=items,
    )


def print_text(result: AuditResult) -> None:
    print(f"PersonalOS Skillify audit: {result.target}")
    print(f"ok: {str(result.ok).lower()}")
    print(f"pass: {result.passed}")
    print(f"fail: {result.failed}")
    print(f"warn: {result.warnings}")
    print(f"not_applicable: {result.not_applicable}")
    print()
    for item in result.items:
        print(f"{item.status.upper()} {item.name}: {item.detail}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit a PersonalOS skill against the Skillify checklist.")
    parser.add_argument("target", help="Skill slug, skill directory, or SKILL.md path.")
    parser.add_argument("--root", default=str(default_root()), help="PersonalOS root. Defaults to this checkout.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--skip-global-check", action="store_true", help="Skip system/checks/system/scripts/check-resolvable.py.")
    args = parser.parse_args(argv)

    result = audit_skill(Path(args.root), args.target, run_global_check=not args.skip_global_check)
    if args.json:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print_text(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
