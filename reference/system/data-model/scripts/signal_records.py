#!/usr/bin/env python3
"""Registry-owned renderer for dated external-signal digests and evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import uuid
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

from pos_v1 import Contract


ALLOWED_KINDS = {"news", "creator-x", "creator-youtube", "weekly-synthesis"}
ALLOWED_OUTCOMES = {"success", "partial", "failed", "stale", "empty"}


def deterministic_uuid7(stable_key: str, occurred_at: datetime) -> str:
    timestamp_ms = int(occurred_at.timestamp() * 1000) & ((1 << 48) - 1)
    digest = hashlib.sha256(stable_key.encode("utf-8")).digest()
    value = timestamp_ms << 80
    value |= 0x7 << 76
    value |= (int.from_bytes(digest[:2], "big") & ((1 << 12) - 1)) << 64
    value |= 0b10 << 62
    value |= int.from_bytes(digest[2:10], "big") & ((1 << 62) - 1)
    return str(uuid.UUID(int=value))


def _datetime(value: datetime | str, field: str) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a UTC offset")
    return parsed.replace(microsecond=0)


def _date(value: date | str, field: str) -> date:
    try:
        return value if isinstance(value, date) else date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date") from exc


def _plain(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text or "\n" in text or "\r" in text:
        raise ValueError(f"{field} must be one non-empty line")
    return text


def _body(value: Any, field: str, default: str | None = None) -> str:
    text = str(value or default or "").strip()
    if not text:
        raise ValueError(f"{field} must not be empty")
    return text


def _slug(value: Any, field: str) -> str:
    text = _plain(value, field)
    if not all(part.isalnum() and part == part.lower() for part in text.split("-")):
        raise ValueError(f"{field} must use lower kebab case")
    return text


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _validate(root: Path, path: Path, text: str) -> None:
    logical_path = path.relative_to(root).as_posix()
    failures = [
        finding
        for finding in Contract(root).validate_text(text, logical_path, resolve_relations=True)
        if finding.level == "fail"
    ]
    if failures:
        detail = "; ".join(f"{item.code}: {item.message}" for item in failures)
        raise ValueError(f"Invalid signal record `{logical_path}`: {detail}")


def materialize_signal_digest(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    producer = _slug(record.get("producer"), "producer")
    digest_date = _date(record.get("digest_date"), "digest_date")
    kind = _plain(record.get("digest_kind"), "digest_kind")
    outcome = _plain(record.get("digest_outcome"), "digest_outcome")
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"Unknown digest_kind: {kind}")
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError(f"Unknown digest_outcome: {outcome}")
    started = _datetime(record.get("coverage_started_at"), "coverage_started_at")
    ended = _datetime(record.get("coverage_ended_at"), "coverage_ended_at")
    if ended < started:
        raise ValueError("coverage_ended_at must not precede coverage_started_at")
    title = _plain(record.get("title"), "title")
    identity_time = datetime.combine(digest_date, time.min, tzinfo=started.tzinfo)
    record_id = deterministic_uuid7(f"signal-digest:{producer}:{digest_date.isoformat()}", identity_time)
    path = root / "interactions" / "signals" / producer / str(digest_date.year) / f"{digest_date.isoformat()}.md"
    updated = _date(record.get("updated") or digest_date, "updated")
    optional = []
    for key in ("source_system", "source_channel"):
        if record.get(key):
            optional.append(f"{key}: {json.dumps(_plain(record[key], key), ensure_ascii=False)}")
    text = "\n".join(
        [
            "---",
            "schema_version: pos-v1",
            f"id: {record_id}",
            "type: signal-digest",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"created: {digest_date.isoformat()}",
            f"updated: {updated.isoformat()}",
            f"digest_date: {digest_date.isoformat()}",
            f"digest_kind: {kind}",
            f"digest_outcome: {outcome}",
            f"coverage_started_at: {started.isoformat()}",
            f"coverage_ended_at: {ended.isoformat()}",
            f"producer_skill_ref: {json.dumps(f'[[skills/{producer}/SKILL]]')}",
            *optional,
            "---",
            "",
            f"# {title}",
            "",
            "## Digest Summary",
            "",
            _body(record.get("digest_summary"), "digest_summary"),
            "",
            "## Coverage",
            "",
            _body(record.get("coverage"), "coverage"),
            "",
            "## Signals",
            "",
            _body(record.get("signals"), "signals", "Keine Signale."),
            "",
            "## Source Map",
            "",
            _body(record.get("source_map"), "source_map", "Keine Quellen."),
            "",
            "## Propagation",
            "",
            _body(record.get("propagation"), "propagation", "Keine automatische Übernahme in einen fachlichen Owner."),
            "",
            "## Gaps and Corrections",
            "",
            _body(record.get("gaps_and_corrections"), "gaps_and_corrections", "Keine bekannten Lücken."),
            "",
        ]
    )
    _validate(root, path, text)
    changed = not path.exists() or path.read_text(encoding="utf-8") != text
    if changed:
        _atomic_write(path, text)
    return {
        "path": str(path),
        "ref": f"[[{path.relative_to(root).with_suffix('').as_posix()}]]",
        "id": record_id,
        "changed": changed,
    }


def signal_companion_directory(root: Path, producer: str, digest_date: date | str) -> Path:
    owner = _slug(producer, "producer")
    day = _date(digest_date, "digest_date")
    return root / "interactions" / "signals" / owner / str(day.year) / day.isoformat()


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write one technical companion without exposing partial JSON."""

    _atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def demote_markdown_headings(markdown: str, minimum_level: int = 3) -> str:
    """Nest a body below a profile-owned H2 section without extra H1/H2 owners."""

    if minimum_level < 1 or minimum_level > 6:
        raise ValueError("minimum_level must be between 1 and 6")
    output = []
    for line in markdown.splitlines():
        level = len(line) - len(line.lstrip("#"))
        if level and level <= 6 and len(line) > level and line[level] == " ":
            target = min(6, max(minimum_level, level + 1))
            line = "#" * target + line[level:]
        output.append(line)
    return "\n".join(output)


def materialize_signal_source_evidence(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Create one immutable Source Evidence record below a dated digest."""

    producer = _slug(record.get("producer"), "producer")
    digest_date = _date(record.get("digest_date"), "digest_date")
    captured_at = _datetime(record.get("evidence_captured_at"), "evidence_captured_at")
    stable_key = _plain(record.get("stable_key"), "stable_key")
    title = _plain(record.get("title"), "title")
    evidence_kind = _plain(record.get("evidence_kind") or "source-card", "evidence_kind")
    if evidence_kind not in {"transcript", "message-batch", "source-card", "asset-pointer", "visual-context", "audio-transcript", "research"}:
        raise ValueError(f"Unknown evidence_kind: {evidence_kind}")
    redaction_mode = _plain(record.get("redaction_mode") or "none", "redaction_mode")
    if redaction_mode not in {"none", "minimized", "redacted"}:
        raise ValueError(f"Unknown redaction_mode: {redaction_mode}")
    digest_path = root / "interactions" / "signals" / producer / str(digest_date.year) / f"{digest_date.isoformat()}.md"
    if not digest_path.exists():
        raise ValueError(f"Signal digest must exist before its evidence: {digest_path.relative_to(root)}")
    identity_time = datetime.combine(digest_date, time.min, tzinfo=captured_at.tzinfo)
    record_id = deterministic_uuid7(f"signal-evidence:{producer}:{stable_key}", identity_time)
    path = signal_companion_directory(root, producer, digest_date) / "evidence" / f"{record_id}.md"
    interaction_ref = f"[[{digest_path.relative_to(root).with_suffix('').as_posix()}]]"
    day = captured_at.date().isoformat()
    text = "\n".join(
        [
            "---",
            "schema_version: pos-v1",
            f"id: {record_id}",
            "type: source-evidence",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"created: {day}",
            f"updated: {day}",
            f"evidence_kind: {evidence_kind}",
            f"evidence_captured_at: {captured_at.isoformat()}",
            f"source_system: {json.dumps(_plain(record.get('source_system'), 'source_system'), ensure_ascii=False)}",
            f"source_ref: {json.dumps(_plain(record.get('source_ref'), 'source_ref'), ensure_ascii=False)}",
            f"interaction_ref: {json.dumps(interaction_ref)}",
            f"redaction_mode: {redaction_mode}",
            "---",
            "",
            f"# {title}",
            "",
            "## Evidence Summary",
            "",
            _body(record.get("evidence_summary"), "evidence_summary"),
            "",
            "## Source Boundary",
            "",
            _body(record.get("source_boundary"), "source_boundary"),
            "",
            "## Evidence",
            "",
            _body(record.get("evidence"), "evidence"),
            "",
            "## Corrections",
            "",
            _body(record.get("corrections"), "corrections", "Keine bekannten Korrekturen."),
            "",
        ]
    )
    _validate(root, path, text)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"Signal evidence identity collision: {path.relative_to(root)}")
        created = False
    else:
        _atomic_write(path, text)
        created = True
    return {
        "path": str(path),
        "ref": f"[[{path.relative_to(root).with_suffix('').as_posix()}]]",
        "id": record_id,
        "created": created,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["materialize-digest", "materialize-evidence"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Input must be one JSON object")
    if args.operation == "materialize-digest":
        result = materialize_signal_digest(args.root, payload)
    else:
        result = materialize_signal_source_evidence(args.root, payload)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
