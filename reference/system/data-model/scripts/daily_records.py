#!/usr/bin/env python3
"""Small rendering helper for admitted modular Daily records.

Workflow ownership stays with the calling skill. This module only materializes the
registered Daily profiles consistently and validates every generated record.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Iterable

from pos_v1 import Contract, uuid7
from time_context import resolve_timezone


def deterministic_uuid7(stable_key: str, occurred_at: datetime) -> str:
    timestamp_ms = int(occurred_at.timestamp() * 1000) & ((1 << 48) - 1)
    digest = hashlib.sha256(stable_key.encode("utf-8")).digest()
    value = timestamp_ms << 80
    value |= 0x7 << 76
    value |= (int.from_bytes(digest[:2], "big") & ((1 << 12) - 1)) << 64
    value |= 0b10 << 62
    value |= int.from_bytes(digest[2:10], "big") & ((1 << 62) - 1)
    return str(uuid.UUID(int=value))


def wikilink(path: str, label: str | None = None) -> str:
    clean = path.removesuffix(".md")
    return f"[[{clean}|{label}]]" if label else f"[[{clean}]]"


def _yaml_list(values: Iterable[str]) -> str:
    return json.dumps(list(dict.fromkeys(values)), ensure_ascii=False)


def _validate(root: Path, path: Path, text: str, *, resolve_relations: bool = True) -> None:
    contract = Contract(root)
    logical_path = path.relative_to(root).as_posix()
    failures = [
        finding
        for finding in contract.validate_text(text, logical_path, resolve_relations=resolve_relations)
        if finding.level == "fail"
    ]
    if failures:
        details = "; ".join(f"{item.code}: {item.message}" for item in failures)
        raise ValueError(f"Invalid Daily record `{logical_path}`: {details}")


def _day_path(root: Path, day_date: str) -> Path:
    return root / "daily" / day_date[:4] / day_date / f"{day_date}.md"


def _render_empty_day(day_date: str, record_id: str, timezone: str) -> str:
    return f'''---
schema_version: pos-v1
id: {record_id}
type: day-record
title: "Day Record - {day_date}"
created: {day_date}
updated: {day_date}
day_date: {day_date}
timezone: {timezone}
---

# Day Record - {day_date}

## Day Summary

Materielle Aktivitäten oder persönliche Einträge dieses Tages werden hier kompakt verknüpft.

## Key Outcomes

- None.

## Activity Contributions

- None.

## Journal

- None.

## Affected Owners

- None.

## Sources

- None.

## Corrections

None.
'''


def ensure_day_record(root: Path, day_date: str, timezone: str | None = None) -> Path:
    path = _day_path(root, day_date)
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    resolved_timezone = resolve_timezone(root, timezone)
    text = _render_empty_day(day_date, uuid7(), resolved_timezone.key)
    _validate(root, path, text, resolve_relations=False)
    path.write_text(text, encoding="utf-8")
    return path


def _upsert_frontmatter_list(text: str, field: str, values: list[str]) -> str:
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0:
        raise ValueError("Day Record has invalid frontmatter delimiters")
    head = text[4:end]
    body = text[end + 5 :]
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.M)
    match = pattern.search(head)
    current: list[str] = []
    if match:
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Unsupported `{field}` representation") from exc
        if not isinstance(parsed, list):
            raise ValueError(f"`{field}` must be a list")
        current = [str(item) for item in parsed]
    merged = list(dict.fromkeys(current + values))
    replacement = f"{field}: {_yaml_list(merged)}"
    if match:
        head = pattern.sub(replacement, head, count=1)
    else:
        head = head.rstrip() + "\n" + replacement
    return "---\n" + head + "\n---\n" + body


def _update_date(text: str, value: str) -> str:
    return re.sub(r"^updated:\s*.+$", f"updated: {value}", text, count=1, flags=re.M)


def _append_section_bullets(text: str, heading: str, bullets: Iterable[str]) -> str:
    additions = [f"- {item}" for item in dict.fromkeys(bullets) if item]
    if not additions:
        return text
    pattern = re.compile(rf"(^## {re.escape(heading)}\n\n)(.*?)(?=\n## |\Z)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Day Record missing section `{heading}`")
    existing = match.group(2).strip()
    lines = [] if existing in {"", "- None.", "None."} else existing.splitlines()
    for addition in additions:
        if addition not in lines:
            lines.append(addition)
    replacement = match.group(1) + "\n".join(lines).rstrip() + "\n"
    return text[: match.start()] + replacement + text[match.end() :]


def link_activity_to_day(
    root: Path,
    day_path: Path,
    activity_path: Path,
    *,
    outcome_summary: str,
    affected_owner_refs: list[str],
    evidence_refs: list[str],
    updated: str,
) -> None:
    text = day_path.read_text(encoding="utf-8")
    activity_ref = wikilink(activity_path.relative_to(root).as_posix())
    text = _upsert_frontmatter_list(text, "activity_refs", [activity_ref])
    text = _update_date(text, updated)
    text = _append_section_bullets(text, "Key Outcomes", [outcome_summary])
    text = _append_section_bullets(text, "Activity Contributions", [activity_ref])
    text = _append_section_bullets(text, "Affected Owners", affected_owner_refs)
    text = _append_section_bullets(text, "Sources", evidence_refs or [activity_ref])
    _validate(root, day_path, text)
    day_path.write_text(text, encoding="utf-8")


def record_activity(
    root: Path,
    *,
    occurred_at: datetime,
    recorded_at: datetime,
    producer_kind: str,
    producer_name: str,
    title: str,
    activity: str,
    outcome: str,
    activity_outcome: str,
    affected_owner_refs: list[str],
    evidence_refs: list[str] | None = None,
    runtime_name: str | None = None,
    producer_ref: str | None = None,
    stable_key: str | None = None,
    timezone: str | None = None,
) -> dict[str, object]:
    if occurred_at.tzinfo is None or recorded_at.tzinfo is None:
        raise ValueError("Daily timestamps must include a UTC offset")
    if not affected_owner_refs:
        raise ValueError("Activity Contributions require at least one affected owner")
    occurred_at = occurred_at.replace(microsecond=0)
    recorded_at = recorded_at.replace(microsecond=0)
    resolved_timezone = resolve_timezone(root, timezone)
    local_occurred_at = occurred_at.astimezone(resolved_timezone)
    local_recorded_at = recorded_at.astimezone(resolved_timezone)
    day_date = local_occurred_at.date().isoformat()
    record_id = deterministic_uuid7(stable_key, occurred_at) if stable_key else uuid7()
    day_path = ensure_day_record(root, day_date, resolved_timezone.key)
    activity_path = day_path.parent / "activity" / f"{record_id}.md"
    evidence_refs = list(dict.fromkeys(evidence_refs or []))
    duplicate = activity_path.exists()
    if not duplicate:
        fields = [
            "---",
            "schema_version: pos-v1",
            f"id: {record_id}",
            "type: activity-contribution",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"created: {day_date}",
            f"updated: {local_recorded_at.date().isoformat()}",
            f"day_date: {day_date}",
            f"timezone: {resolved_timezone.key}",
            f"occurred_at: {occurred_at.isoformat(timespec='seconds')}",
            f"recorded_at: {recorded_at.isoformat(timespec='seconds')}",
            f"producer_kind: {producer_kind}",
            f"producer_name: {json.dumps(producer_name, ensure_ascii=False)}",
        ]
        if runtime_name:
            fields.append(f"runtime_name: {json.dumps(runtime_name, ensure_ascii=False)}")
        if producer_ref:
            fields.append(f"producer_ref: {json.dumps(producer_ref, ensure_ascii=False)}")
        fields.extend([
            f"activity_outcome: {activity_outcome}",
            f"affected_owner_refs: {_yaml_list(affected_owner_refs)}",
        ])
        if evidence_refs:
            fields.append(f"evidence_refs: {_yaml_list(evidence_refs)}")
        fields.extend([
            "---",
            "",
            f"# {title}",
            "",
            "## Activity",
            "",
            activity.strip(),
            "",
            "## Outcome",
            "",
            outcome.strip(),
            "",
            "## Affected Owners",
            "",
            *(f"- {item}" for item in affected_owner_refs),
            "",
            "## Evidence",
            "",
            *(f"- {item}" for item in (evidence_refs or ["Direkter Producer-Beleg."])),
            "",
            "## Corrections",
            "",
            "None.",
            "",
        ])
        text = "\n".join(fields)
        _validate(root, activity_path, text)
        activity_path.parent.mkdir(parents=True, exist_ok=True)
        activity_path.write_text(text, encoding="utf-8")
    link_activity_to_day(
        root,
        day_path,
        activity_path,
        outcome_summary=outcome,
        affected_owner_refs=affected_owner_refs,
        evidence_refs=evidence_refs,
        updated=local_recorded_at.date().isoformat(),
    )
    return {
        "path": activity_path,
        "day_path": day_path,
        "id": record_id,
        "duplicate": duplicate,
    }
