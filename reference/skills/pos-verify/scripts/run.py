#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_SKILL_FRONTMATTER = ("name", "version", "description", "triggers", "tools", "mutating")
REQUIRED_SKILL_SECTIONS = (
    "## Contract",
    "## Phases",
    "## Output Format",
    "## Anti-Patterns",
    "## Tools Used",
)
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
ENTITY_PREFIXES = ("people/", "companies/", "deals/", "projects/", "programs/")
V1_CANONICAL_PREFIXES = ("people/", "companies/", "deals/", "projects/", "programs/")
V1_LEGACY_PREFIXES = ("organisations/",)
YAML_LIST_FIELDS = ("tags", "aliases", "primary_contacts")
PLACEHOLDER_MARKER = "Migrated placeholder."
FORBIDDEN_V1_FIELDS = {
    "legacy_type",
    "legacy_path",
    "repo_artifacts",
    "artifact_root",
    "project_area",
    "repo_local_path",
}
V1_BASE_REQUIRED = ("schema_version", "type", "pos_domain", "role", "status", "title", "updated", "tags")
V1_PROFILE_RULES = {
    "person": {
        "hard_max": 20,
        "required_fields": V1_BASE_REQUIRED,
        "required_sections": (
            "Current Truth",
            "State",
            "What They Build",
            "Beliefs / Thinking",
            "Communication Profile",
            "Relationship",
            "Network",
            "Open Threads",
            "See Also",
            "Timeline",
        ),
    },
    "company": {
        "hard_max": 20,
        "required_fields": V1_BASE_REQUIRED,
        "required_sections": (
            "Current Truth",
            "State",
            "Business Model",
            "People",
            "Decision Logic",
            "Relationship",
            "Risks / Tensions",
            "Open Threads",
            "See Also",
            "Timeline",
        ),
    },
    "deal": {
        "hard_max": 22,
        "required_fields": V1_BASE_REQUIRED,
        "required_sections": (
            "Current Truth",
            "State",
            "Commercial Frame",
            "Stakeholders",
            "Decision / Next Gate",
            "Source Map",
            "Open Threads",
            "See Also",
            "Timeline",
        ),
    },
    "project": {
        "hard_max": 22,
        "required_fields": V1_BASE_REQUIRED,
        "required_sections": (
            "Current Truth",
            "State",
            "Scope Boundary",
            "Repo / External Truth",
            "Stakeholders",
            "Decisions",
            "Open Threads",
            "See Also",
            "Timeline",
        ),
        "forbidden_sections": ("Kurzstatus", "Aktueller Stand"),
    },
    "program": {
        "hard_max": 20,
        "required_fields": V1_BASE_REQUIRED,
        "required_sections": (
            "Current Truth",
            "State",
            "Strategy",
            "Active Projects",
            "Operating Rhythm",
            "Open Threads",
            "See Also",
            "Timeline",
        ),
    },
    "source": {
        "hard_max": 28,
        "required_fields": ("schema_version", "type", "pos_domain", "role", "status", "title", "updated", "tags"),
        "required_sections": ("Summary",),
        "alternative_sections": {"Summary": ("Summary", "Source Summary", "Payload")},
    },
    "automation-output": {
        "hard_max": 32,
        "required_fields": (
            "schema_version",
            "type",
            "pos_domain",
            "subtype",
            "role",
            "status",
            "title",
            "automation",
            "run_date",
            "run_status",
            "run_trigger",
            "briefing_include",
            "briefing_section",
            "summary",
            "priority",
            "updated",
            "tags",
        ),
        "required_sections": (),
    },
    "data-record": {
        "hard_max": 42,
        "required_fields": ("schema_version", "type", "pos_domain", "role", "status", "title", "updated", "tags", "profile"),
        "required_sections": (),
    },
}
LINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:[#\|][^\]]*)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
EXTERNAL_MARKDOWN_LINK_PREFIXES = ("http://", "https://", "mailto:", "obsidian:", "file:", "/", "#", "data:")
FENCED_CODE_RE = re.compile(r"(^|\n)```.*?(?=\n```|\Z)\n?```?", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
_POS_V1_CONTRACTS: dict[str, object] = {}
MarkdownFrontmatter = tuple[dict[str, str], bool, str, bool]


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str
    remediation: str


def repo_root(script_path: Path | None = None) -> Path:
    """Resolve the owning PersonalOS vault before falling back to the caller CWD."""
    script = (script_path or Path(__file__)).resolve()
    for candidate in script.parents:
        verifier = candidate / "skills" / "pos-verify" / "scripts" / "run.py"
        if (candidate / "INDEX.md").is_file() and verifier.is_file():
            return candidate

    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return Path(proc.stdout.strip())
    return Path.cwd()


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def active_markdown_text(text: str) -> str:
    """Return Markdown text with code examples removed before link checks."""
    text = FENCED_CODE_RE.sub("\n", text)
    return INLINE_CODE_RE.sub("", text)


def frontmatter_raw(text: str) -> tuple[str, bool]:
    if not text.startswith("---\n"):
        return "", False
    end = text.find("\n---", 4)
    if end == -1:
        return "", False
    return text[4:end], True


def frontmatter(text: str) -> tuple[dict[str, str], bool]:
    raw, ok = frontmatter_raw(text)
    if not ok:
        return {}, False
    data: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip().strip("\"'")
        if value not in {"|", ">"}:
            data[key] = value
        else:
            data[key] = value
    return data, True


def markdown_frontmatter(text: str) -> MarkdownFrontmatter:
    raw, has_raw = frontmatter_raw(text)
    if not has_raw:
        return {}, False, raw, has_raw
    data, has_frontmatter = frontmatter(text)
    return data, has_frontmatter, raw, has_raw


def declares_pos_v1(text: str, fm: dict[str, str] | None = None) -> bool:
    """Recognize ordinary pos-v1 records and the registered SKILL.md runtime envelope."""
    parsed = fm or {}
    if parsed.get("schema_version") == "pos-v1":
        return True
    raw, has_raw = frontmatter_raw(text)
    return bool(
        has_raw
        and re.search(r"^\s+pos_schema_version:\s*['\"]?pos-v1['\"]?\s*$", raw, re.M)
    )


def pos_v1_record_id(text: str, fm: dict[str, str] | None = None) -> str | None:
    """Return the stable ID from ordinary or runtime-enveloped pos-v1 frontmatter."""
    parsed = fm or {}
    if parsed.get("schema_version") == "pos-v1":
        return parsed.get("id")
    if not declares_pos_v1(text, parsed):
        return None
    raw, _ = frontmatter_raw(text)
    match = re.search(r"^\s+pos_id:\s*['\"]?([0-9a-f-]+)['\"]?\s*$", raw, re.M)
    return match.group(1) if match else None


def heading_names(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.M)]


def section_body(text: str, heading: str) -> str:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+.+?\s*$", text[match.end() :], re.M)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def markdown_word_count(text: str) -> int:
    cleaned = active_markdown_text(text)
    cleaned = re.sub(r"\[\[|\]\]|\[[^\]]*\]\([^)]*\)", " ", cleaned)
    return len(re.findall(r"\b[\wÄÖÜäöüß'-]+\b", cleaned, re.UNICODE))


def markdown_bullet_count(text: str) -> int:
    return len(re.findall(r"^\s*-\s+", active_markdown_text(text), re.M))


def section_present(headings: set[str], allowed: tuple[str, ...]) -> bool:
    for heading in headings:
        for item in allowed:
            if heading == item or heading.startswith(f"{item} /"):
                return True
    return False


def v1_profile(path: Path, root: Path, fm: dict[str, str]) -> str | None:
    r = rel(path, root)
    page_type = fm.get("type", "")
    role = fm.get("role", "")
    subtype = fm.get("subtype", "")
    profile = fm.get("profile", "")

    if path.name == "index.md" and (role == "index" or page_type == "note"):
        return None
    if profile == "data-record":
        return "data-record"
    if r.startswith("people/") or page_type == "person":
        return "person"
    if r.startswith("companies/") or page_type == "company":
        return "company"
    if r.startswith("deals/") or page_type == "deal":
        return "deal"
    if r.startswith("programs/") or (page_type == "project" and (subtype == "program" or role == "program")):
        return "program"
    if r.startswith("projects/") or page_type == "project":
        return "project"
    if page_type == "source" and role == "run-report":
        return "source"
    if "/outputs/" in f"/{r}/" or "/_system/runs/" in f"/{r}/" or fm.get("automation"):
        return "automation-output"
    if page_type == "source" or r.startswith("sources/"):
        return "source"
    return None


def check_v1_profile(path: Path, root: Path, text: str, fm: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    r = rel(path, root)

    if r.startswith(V1_LEGACY_PREFIXES):
        findings.append(
            Finding(
                "fail",
                "v1_legacy_directory",
                r,
                "V1 canonical file remains under a legacy directory.",
                "Move organisations/ canonical files to companies/ and update links.",
            )
        )

    if fm.get("schema_version") not in {"pos-gbrain-v1", "pos-v1"} and r.startswith(V1_CANONICAL_PREFIXES):
        findings.append(
            Finding(
                "warn",
                "canonical_not_v1",
                r,
                "Canonical Gbrain-v1 path does not use schema_version: pos-gbrain-v1.",
                "Migrate this file's frontmatter to pos-gbrain-v1.",
            )
        )
        return findings

    if fm.get("schema_version") != "pos-gbrain-v1":
        return findings

    for key in sorted(FORBIDDEN_V1_FIELDS & set(fm)):
        findings.append(
            Finding(
                "fail",
                "v1_forbidden_frontmatter_field",
                r,
                f"V1 file contains forbidden legacy field: {key}",
                "Remove the legacy field or move durable content into the body if it is still needed.",
            )
        )

    profile = v1_profile(path, root, fm)
    if profile is None:
        return findings

    if PLACEHOLDER_MARKER in text:
        findings.append(
            Finding(
                "fail",
                "v1_placeholder_content",
                r,
                "V1 profile still contains mechanical migration placeholder content.",
                "Replace the placeholder with deterministic section content or migrate real existing content into the v1 section.",
            )
        )

    rules = V1_PROFILE_RULES.get(profile, {})
    if profile == "automation-output":
        if fm.get("type") != "source":
            findings.append(
                Finding(
                    "fail",
                    "v1_automation_output_type",
                    r,
                    "Automation output must use type: source.",
                    "Use `type: source` and `subtype: automation-output`; legacy `type: automation-output` remains readable but is not the canonical v1 profile.",
                )
            )
        if fm.get("subtype") != "automation-output":
            findings.append(
                Finding(
                    "fail",
                    "v1_automation_output_subtype",
                    r,
                    "Automation output must use subtype: automation-output.",
                    "Set `subtype: automation-output` in frontmatter.",
                )
            )
    for key in rules.get("required_fields", ()):
        if key not in fm:
            findings.append(
                Finding(
                    "fail",
                    "v1_missing_required_field",
                    r,
                    f"{profile} profile missing required frontmatter field: {key}",
                    f"Add `{key}` to the file frontmatter.",
                )
            )

    field_count = len(fm)
    hard_max = int(rules.get("hard_max", 0) or 0)
    if hard_max and field_count > hard_max:
        findings.append(
            Finding(
                "warn",
                "v1_frontmatter_field_count",
                r,
                f"{profile} profile has {field_count} frontmatter fields; hard max is {hard_max}.",
                "Move non-routing/query details into the markdown body or mark true structured records as profile: data-record.",
            )
        )

    headings = heading_names(text)
    heading_set = set(headings)
    alternatives = rules.get("alternative_sections", {})
    for section in rules.get("required_sections", ()):
        allowed = alternatives.get(section, (section,))
        if not section_present(heading_set, tuple(allowed)):
            findings.append(
                Finding(
                    "fail",
                    "v1_missing_required_section",
                    r,
                    f"{profile} profile missing required section: ## {section}",
                    f"Add a `## {section}` section or migrate equivalent existing content into it.",
                )
            )

    forbidden_sections = set(rules.get("forbidden_sections", ()))
    if profile in {"person", "company", "deal", "project", "program"}:
        forbidden_sections.update({"Kurzstatus", "Aktueller Stand"})

    for section in sorted(forbidden_sections):
        if section in heading_set:
            findings.append(
                Finding(
                    "fail",
                    "v1_forbidden_section",
                    r,
                    f"{profile} profile still contains forbidden legacy section: ## {section}",
                    "Migrate this section into the v1 Current Truth, State, or another profile section.",
                )
            )

    if profile in {"person", "company", "deal", "project", "program"}:
        current_truth = section_body(text, "Current Truth")
        current_truth_words = markdown_word_count(current_truth)
        current_truth_limit = 500 if profile in {"person", "company"} else 400
        if current_truth_words > current_truth_limit:
            findings.append(
                Finding(
                    "warn",
                    "current_truth_overlong",
                    r,
                    f"Current Truth has {current_truth_words} words; the {profile} rewrite warning threshold is {current_truth_limit}.",
                    "Rewrite Current Truth as a short present-state synthesis; move chronology to Timeline and detail to State, sources, artifacts or repo truth.",
                )
            )

        state_bullets = markdown_bullet_count(section_body(text, "State"))
        if state_bullets > 12:
            findings.append(
                Finding(
                    "warn",
                    "state_too_many_bullets",
                    r,
                    f"State has {state_bullets} bullets; the high-signal budget is 12.",
                    "Merge or move low-level detail so State keeps only the current high-signal operating picture.",
                )
            )

        open_thread_bullets = markdown_bullet_count(section_body(text, "Open Threads"))
        if open_thread_bullets > 10:
            findings.append(
                Finding(
                    "warn",
                    "open_threads_too_many_bullets",
                    r,
                    f"Open Threads has {open_thread_bullets} bullets; the outcome-level budget is 10.",
                    "Keep only unresolved outcome-level gates, risks or missing inputs; route executable next actions through task-manager to operations/actions/.",
                )
            )

    if profile == "project" and re.search(r"^\s*-\s+\[[ xX]\]\s+", active_markdown_text(text), re.M):
        findings.append(
            Finding(
                "warn",
                "project_shadow_task_list",
                r,
                "Project page contains checkbox tasks and therefore creates a shadow action list.",
                "Classify each checkbox as durable project state, atomic operations/actions record, repo item, completed history or stale noise before removing it.",
            )
        )

    if profile in {"person", "company", "deal", "project", "program"}:
        if re.search(r"^##\s+Timeline\s*\n\s*\|", active_markdown_text(text), re.M):
            findings.append(
                Finding(
                    "fail",
                    "v1_timeline_table",
                    r,
                    "V1 canonical timeline still uses a Markdown table.",
                    "Convert `## Timeline` to append-only bullet entries: `- **YYYY-MM-DD** | Source/context - Entry`.",
                )
            )

    if headings.count("Timeline") > 1:
        findings.append(
            Finding(
                "fail",
                "v1_duplicate_timeline",
                r,
                "V1 canonical file has duplicate Timeline sections.",
                "Merge timeline content into one append-only `## Timeline` section.",
            )
        )

    if profile == "program":
        if fm.get("type") != "project" or fm.get("subtype") != "program" or fm.get("role") != "program":
            findings.append(
                Finding(
                    "fail",
                    "v1_invalid_program_frontmatter",
                    r,
                    "Program files must use type: project, subtype: program, role: program.",
                    "Update program frontmatter to the v1 program profile.",
                )
            )

    return findings


def load_pos_v1_contract(root: Path, runtime_path: Path) -> object:
    key = str(root.resolve())
    contract = _POS_V1_CONTRACTS.get(key)
    if contract is not None:
        return contract
    spec = importlib.util.spec_from_file_location(f"pos_v1_runtime_{abs(hash(key))}", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load pos-v1 runtime module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    runtime_dir = str(runtime_path.resolve().parent)
    added_runtime_dir = runtime_dir not in sys.path
    if added_runtime_dir:
        sys.path.insert(0, runtime_dir)
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    finally:
        if added_runtime_dir:
            sys.path.remove(runtime_dir)
    contract = module.Contract(root)
    _POS_V1_CONTRACTS[key] = contract
    return contract


def check_pos_v1_contract(path: Path, root: Path, text: str, fm: dict[str, str]) -> list[Finding]:
    if not declares_pos_v1(text, fm):
        return []
    runtime_path = root / "system" / "data-model" / "scripts" / "pos_v1.py"
    if not runtime_path.is_file():
        return [
            Finding(
                "fail",
                "pos_v1_runtime_missing",
                rel(path, root),
                "Record declares pos-v1 but the registry runtime is missing.",
                "Restore system/data-model/scripts/pos_v1.py before writing pos-v1 records.",
            )
        ]
    try:
        contract = load_pos_v1_contract(root, runtime_path)
        runtime_findings = contract.validate_text(text, rel(path, root))
    except Exception as exc:
        return [
            Finding(
                "fail",
                "pos_v1_registry_error",
                rel(path, root),
                f"pos-v1 registry or runtime failed: {exc}",
                "Run `python3 system/data-model/scripts/pos_v1.py --root . check-registry` and repair the central contract.",
            )
        ]
    return [Finding(item.level, item.code, item.path, item.message, item.remediation) for item in runtime_findings]


def markdown_files(root: Path) -> list[Path]:
    skip = {".git", ".obsidian", ".trash", "node_modules", "__pycache__"}
    files: list[Path] = []
    for path in root.rglob("*.md"):
        try:
            parts = set(path.relative_to(root).parts)
        except ValueError:
            continue
        if parts & skip:
            continue
        files.append(path)
    return files


def alias_index(root: Path) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for path in markdown_files(root):
        r = rel(path, root)
        index.setdefault(path.stem, []).append(r)
        text = read_text(path)
        fm, _ = frontmatter(text)
        raw_aliases = fm.get("aliases", "")
        if raw_aliases.startswith("[") and raw_aliases.endswith("]"):
            for alias in raw_aliases[1:-1].split(","):
                alias = alias.strip().strip("\"'")
                if alias:
                    index.setdefault(alias, []).append(r)
    return index


def git_changed(root: Path) -> list[Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    names: set[str] = set()
    for command in commands:
        proc = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if proc.returncode == 0:
            names.update(line.strip() for line in proc.stdout.splitlines() if line.strip())
    return [root / name for name in sorted(names)]


def normalize_files(root: Path, raw_files: list[str], changed_from: str | None) -> tuple[list[Path], list[Finding]]:
    findings: list[Finding] = []
    paths: list[Path] = []
    if raw_files:
        paths = [Path(item) for item in raw_files]
    elif changed_from == "git":
        paths = git_changed(root)
        if len(paths) > 50:
            findings.append(
                Finding(
                    "warn",
                    "large_git_discovery",
                    ".",
                    f"Git discovery found {len(paths)} changed files; this may include unrelated dirty-tree work.",
                    "Prefer explicit --files from the calling skill or pos-write for write-scoped verification.",
                )
            )
    else:
        findings.append(
            Finding(
                "fail",
                "no_changed_files",
                ".",
                "No changed files were provided and no discovery mode was selected.",
                "Pass --files <path...> or use --changed-from git.",
            )
        )

    normalized: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        candidate = path if path.is_absolute() else root / path
        key = rel(candidate, root)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists() and candidate.is_file():
            normalized.append(candidate)
        else:
            findings.append(
                Finding(
                    "warn",
                    "missing_or_deleted_file",
                    key,
                    "File does not exist at verification time.",
                    "If this was a deliberate delete or move, verify the deletion with the owning skill; otherwise restore or correct the path.",
                )
            )
    return normalized, findings


def check_conflicts(path: Path, root: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    r = rel(path, root)
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith(CONFLICT_MARKERS):
            findings.append(
                Finding(
                    "fail",
                    "conflict_marker",
                    f"{r}:{lineno}",
                    f"Merge conflict marker found: {stripped.split(maxsplit=1)[0]}",
                    "Resolve the conflict marker before finishing the POS write.",
                )
            )
    return findings


def frontmatter_optional(path: Path, root: Path) -> bool:
    r = rel(path, root)
    if r in {"AGENTS.md", "CLAUDE.md"}:
        return True
    if r.startswith("skills/conventions/"):
        return True
    if "/references/" in r or "/outputs/" in r or "/runs/" in r:
        return True
    return False


def check_markdown_integrity(
    path: Path,
    root: Path,
    text: str,
    link_index: dict[str, list[str]],
    *,
    strict_links: bool = False,
    parsed_frontmatter: MarkdownFrontmatter | None = None,
) -> list[Finding]:
    """Run generic Markdown and link assertions owned by markdown-record-integrity."""
    findings: list[Finding] = []
    r = rel(path, root)
    fm, has_fm, raw_fm, has_raw_fm = parsed_frontmatter or markdown_frontmatter(text)
    if not has_fm and not frontmatter_optional(path, root):
        findings.append(
            Finding(
                "warn",
                "missing_frontmatter",
                r,
                "Markdown file has no closed frontmatter block.",
                "Add frontmatter when this file is canonical truth; leave only if the owning skill treats it as a raw/output file.",
            )
        )

    if has_raw_fm:
        for field in YAML_LIST_FIELDS:
            if re.search(rf"^{re.escape(field)}:\s*['\"]\s*\[", raw_fm, re.M):
                findings.append(
                    Finding(
                        "fail" if field == "tags" else "warn",
                        "noncanonical_yaml_list",
                        r,
                        f"Frontmatter field `{field}` is stored as a quoted string instead of a YAML list.",
                        f"Rewrite `{field}` as a real YAML list, e.g. `{field}: []` or `{field}: [\"item\"]`.",
                    )
                )

    if fm.get("schema_version") == "pos-v1" and not r.startswith("skills/"):
        for destination in MARKDOWN_LINK_RE.findall(active_markdown_text(text)):
            normalized = destination.strip().strip("<>")
            if normalized.startswith(EXTERNAL_MARKDOWN_LINK_PREFIXES):
                continue
            findings.append(
                Finding(
                    "fail",
                    "pos_v1_internal_markdown_link",
                    r,
                    f"Internal Markdown link violates the pos-v1 graph contract: ({destination})",
                    "Use a path-qualified Obsidian Wikilink; portable relative Skill resources are the only exception.",
                )
            )

    for raw_target in LINK_RE.findall(active_markdown_text(text)):
        target = raw_target.strip()
        if target.endswith("\\"):
            target = target[:-1].rstrip()
        if not target or "<" in target or ">" in target:
            continue
        matches: list[str] = []
        if "/" in target:
            direct = root / target
            candidates = [direct, direct.with_suffix(".md")]
            # A canonical record may intentionally share its stem with a
            # companion directory (for example ``brand.md`` and ``brand/``).
            # Obsidian resolves the Markdown file; directories are not link
            # targets and must not create a false ambiguity.
            matches = [rel(item, root) for item in candidates if item.is_file()]
            if not matches:
                matches = link_index.get(Path(target).name, [])
        else:
            matches = link_index.get(target, [])
        if not matches:
            findings.append(
                Finding(
                    "warn",
                    "broken_wikilink",
                    r,
                    f"Internal link appears unresolved: [[{target}]]",
                    "Fix the link target or add the missing canonical file/alias if this link is intentional.",
                )
            )
        elif len(set(matches)) > 1 and strict_links:
            findings.append(
                Finding(
                    "warn",
                    "ambiguous_wikilink",
                    r,
                    f"Internal link is ambiguous: [[{target}]] -> {', '.join(sorted(set(matches))[:5])}",
                    "Use a more specific link or resolve duplicate aliases/basenames.",
                )
            )
    return findings


def check_legacy_markdown_compatibility(
    path: Path,
    root: Path,
    text: str,
    parsed_frontmatter: MarkdownFrontmatter | None = None,
) -> list[Finding]:
    """Run explicitly temporary pos-gbrain-v1 compatibility assertions."""
    findings: list[Finding] = []
    r = rel(path, root)
    fm, _, _, _ = parsed_frontmatter or markdown_frontmatter(text)
    is_folder_index = Path(r).name == "index.md" and fm.get("role") == "index"
    if (
        r.startswith(ENTITY_PREFIXES)
        and r.endswith(".md")
        and "/files/" not in r
        and not is_folder_index
        and fm.get("schema_version") != "pos-v1"
    ):
        if "updated" not in fm:
            findings.append(
                Finding(
                    "warn",
                    "missing_updated",
                    r,
                    "Canonical entity/project-like file has no updated field.",
                    "Add or refresh updated: YYYY-MM-DD when the file's current truth changes.",
                )
            )
        if not re.search(r"^##\s+(Current Truth|Aktueller Stand|Current State)\b", text, re.M):
            findings.append(
                Finding(
                    "warn",
                    "missing_current_truth",
                    r,
                    "Canonical entity/project-like file has no Current Truth/Aktueller Stand section.",
                    "Add a current-state section near the top or confirm the owning skill intentionally uses another template.",
                )
            )
        if not re.search(r"^##\s+Timeline\b", text, re.M):
            findings.append(
                Finding(
                    "warn",
                    "missing_timeline",
                    r,
                    "Canonical entity/project-like file has no Timeline section.",
                    "Add a Timeline section for dated evidence and changes.",
                )
            )

    findings.extend(check_v1_profile(path, root, text, fm))
    return findings


def check_markdown(
    path: Path,
    root: Path,
    text: str,
    link_index: dict[str, list[str]],
    *,
    strict_links: bool = False,
    parsed_frontmatter: MarkdownFrontmatter | None = None,
) -> list[Finding]:
    """Compatibility facade that composes checks by their declared verification owner."""
    parsed = parsed_frontmatter or markdown_frontmatter(text)
    fm, _, _, _ = parsed
    findings = check_markdown_integrity(
        path,
        root,
        text,
        link_index,
        strict_links=strict_links,
        parsed_frontmatter=parsed,
    )
    findings.extend(check_pos_v1_contract(path, root, text, fm))
    findings.extend(check_legacy_markdown_compatibility(path, root, text, parsed))
    return findings


def check_legacy_skill_compatibility(
    path: Path,
    root: Path,
    text: str,
    parsed_frontmatter: MarkdownFrontmatter | None = None,
) -> list[Finding]:
    """Run the temporary pos-gbrain-v1 skill-shape compatibility assertions."""
    findings: list[Finding] = []
    r = rel(path, root)
    fm, has_fm, _, _ = parsed_frontmatter or markdown_frontmatter(text)
    if declares_pos_v1(text, fm):
        return findings
    if not has_fm:
        findings.append(
            Finding("fail", "skill_missing_frontmatter", r, "SKILL.md has no frontmatter.", "Add required skill frontmatter.")
        )
        return findings

    for key in REQUIRED_SKILL_FRONTMATTER:
        if key not in fm:
            findings.append(
                Finding(
                    "fail",
                    "skill_missing_frontmatter_field",
                    r,
                    f"SKILL.md frontmatter missing required field: {key}",
                    f"Add `{key}` to the skill frontmatter.",
                )
            )

    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            findings.append(
                Finding(
                    "fail",
                    "skill_missing_section",
                    r,
                    f"SKILL.md missing required section: {section}",
                    f"Add `{section}` with executable instructions.",
                )
            )

    legacy_rule_path = "skills/" + "conventions/"
    if legacy_rule_path in text:
        findings.append(
            Finding(
                "warn",
                "legacy_rule_reference",
                r,
                "Skill still references the legacy conventions folder directly.",
                "Replace the Legacy dependency with its canonical Principle, Rule, Contract, Convention, Framework, Template, Runbook or Check under system/.",
            )
        )

    is_infra = path.parent.name in {"pos-write", "pos-verify", "pos-operations"}
    if fm.get("mutating", "").lower() == "true" and not is_infra:
        has_mutation_contract = (
            "pos-write" in text
            or "system/contracts/core/personalos-mutation-contract" in text
            or "system/runbooks/core/personalos-mutation" in text
        )
        if not has_mutation_contract or "pos-verify" not in text:
            findings.append(
                Finding(
                    "warn",
                    "mutating_skill_missing_pos_loop",
                    r,
                    "Mutating skill does not clearly reference the canonical mutation contract/runbook (or its legacy pos-write adapter) and pos-verify.",
                    "Reference the canonical PersonalOS mutation contract or runbook plus pos-verify, or document a temporary compatibility boundary.",
                )
            )

    return findings


def check_skill(path: Path, root: Path, text: str) -> list[Finding]:
    """Compatibility facade for callers that still use the historical function name."""
    return check_legacy_skill_compatibility(path, root, text)


def check_capability_control_plane_if_needed(root: Path, files: list[Path]) -> list[Finding]:
    """Run resolver health for writes that touch the capability layer."""
    rels = [rel(path, root) for path in files]
    if not any(item.startswith("skills/") for item in rels):
        return []
    script = root / "system" / "checks" / "system" / "scripts" / "check-resolvable.py"
    if not script.exists():
        return [
            Finding(
                "warn",
                "check_resolvable_missing",
                "system/checks/system/scripts/check-resolvable.py",
                "Skill files changed but check-resolvable.py is missing.",
                "Restore the resolver check or verify skill resolver health manually.",
            )
        ]
    proc = subprocess.run(
        ["python3", str(script), "--json"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    if proc.returncode == 0:
        return []
    try:
        payload = json.loads(proc.stdout)
        items = payload.get("findings", [])
    except Exception:
        items = []
    message = "system/checks/system/scripts/check-resolvable.py failed after skill-layer changes."
    if items:
        sample = "; ".join(f"{item.get('code')}: {item.get('path')}" for item in items[:5])
        message = f"{message} Sample: {sample}"
    return [
        Finding(
            "fail",
            "check_resolvable_failed",
            "skills",
            message,
            "Run python3 system/checks/system/scripts/check-resolvable.py and fix resolver/index/routing-eval drift.",
        )
    ]


def check_resolvable_if_needed(root: Path, files: list[Path]) -> list[Finding]:
    """Compatibility facade for the historical resolver-check function name."""
    return check_capability_control_plane_if_needed(root, files)


def check_pos_v1_generated_if_needed(root: Path, files: list[Path]) -> list[Finding]:
    rels = [rel(path, root) for path in files]
    if not any(item.startswith("system/data-model/") and not item.startswith("system/data-model/generated/") for item in rels):
        return []
    runtime = root / "system" / "data-model" / "scripts" / "pos_v1.py"
    if not runtime.is_file():
        return [
            Finding(
                "fail",
                "pos_v1_runtime_missing",
                "system/data-model/scripts/pos_v1.py",
                "Data-model files changed but the pos-v1 runtime is missing.",
                "Restore the Registry runtime before changing the central contract.",
            )
        ]
    try:
        contract = load_pos_v1_contract(root, runtime)
        drift = contract.build_generated(check=True)
    except Exception as exc:
        drift = []
        detail = str(exc)
    else:
        detail = f"Drifted artifacts: {', '.join(drift)}" if drift else ""
    if not drift and not detail:
        return []
    return [
        Finding(
            "fail",
            "pos_v1_generated_drift",
            "system/data-model/generated",
            f"Derived pos-v1 artifacts do not match the canonical Registry. {detail}",
            "Run `python3 system/data-model/scripts/pos_v1.py build`, inspect the generated diff, and verify again.",
        )
    ]


def check_pos_v1_duplicate_ids(
    root: Path,
    files: list[Path],
    file_texts: dict[Path, str] | None = None,
) -> list[Finding]:
    """Check scoped pos-v1 IDs against the vault with one shared filesystem scan."""
    texts = file_texts or {}
    targets: dict[str, list[Path]] = {}
    for path in files:
        if path.suffix != ".md":
            continue
        text = texts.get(path) or read_text(path)
        fm, _, _, _ = markdown_frontmatter(text)
        record_id = pos_v1_record_id(text, fm)
        if record_id:
            targets.setdefault(record_id, []).append(path.resolve())
    if not targets:
        return []

    matches: dict[Path, list[str]] = {path: [] for paths in targets.values() for path in paths}
    for candidate in root.rglob("*.md"):
        resolved = candidate.resolve()
        if any(part in {".git", ".obsidian", "node_modules"} for part in candidate.parts):
            continue
        raw = texts.get(candidate) or read_text(candidate)
        candidate_fm, _, _, _ = markdown_frontmatter(raw)
        record_id = pos_v1_record_id(raw, candidate_fm)
        if record_id not in targets:
            continue
        candidate_path = rel(candidate, root)
        for target_path in targets[record_id]:
            if resolved != target_path:
                matches[target_path].append(candidate_path)

    findings: list[Finding] = []
    for target_path, duplicate_paths in matches.items():
        if not duplicate_paths:
            continue
        record_id = next(record_id for record_id, paths in targets.items() if target_path in paths)
        findings.append(
            Finding(
                "fail",
                "pos_v1_duplicate_id",
                rel(target_path, root),
                f"ID `{record_id}` also occurs in {duplicate_paths}.",
                "Assign a fresh UUIDv7 to the newly created duplicate; never change the established record ID.",
            )
        )
    return findings


def check_global_verification(
    root: Path,
    files: list[Path],
    file_texts: dict[Path, str] | None = None,
) -> list[Finding]:
    """Compose global checks without mixing their declarative ownership."""
    findings = check_capability_control_plane_if_needed(root, files)
    findings.extend(check_pos_v1_generated_if_needed(root, files))
    findings.extend(check_pos_v1_duplicate_ids(root, files, file_texts))
    return findings


def severity(findings: list[Finding]) -> str:
    if any(item.level == "fail" for item in findings):
        return "fail"
    if any(item.level == "warn" for item in findings):
        return "warn"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write-scoped PersonalOS verification.")
    parser.add_argument("--files", nargs="*", default=[], help="Explicit changed files to verify.")
    parser.add_argument("--changed-from", choices=["git"], default=None, help="Discover changed files from Git.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--no-global", action="store_true", help="Skip supporting global checks such as check-resolvable.")
    parser.add_argument("--strict-links", action="store_true", help="Warn on ambiguous wikilinks as well as broken links.")
    args = parser.parse_args()

    root = repo_root()
    files, findings = normalize_files(root, args.files, args.changed_from)
    link_index = alias_index(root)
    file_texts: dict[Path, str] = {}

    for path in files:
        text = read_text(path)
        file_texts[path] = text
        parsed = markdown_frontmatter(text) if path.suffix == ".md" else None
        findings.extend(check_conflicts(path, root, text))
        if path.suffix == ".md":
            findings.extend(
                check_markdown(
                    path,
                    root,
                    text,
                    link_index,
                    strict_links=args.strict_links,
                    parsed_frontmatter=parsed,
                )
            )
        if path.name == "SKILL.md" and "/skills/" in f"/{rel(path, root)}":
            findings.extend(check_legacy_skill_compatibility(path, root, text, parsed))

    if not args.no_global:
        findings.extend(check_global_verification(root, files, file_texts))

    result = {
        "status": severity(findings),
        "checked_files": [rel(path, root) for path in files],
        "finding_count": len(findings),
        "findings": [asdict(item) for item in findings],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"pos-verify: {result['status']} ({len(files)} file(s), {len(findings)} finding(s))")
        for item in findings:
            print(f"[{item.level}] {item.code} {item.path}: {item.message}")
            print(f"      fix: {item.remediation}")

    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
