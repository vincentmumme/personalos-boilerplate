#!/usr/bin/env python3
"""Registry-owned renderer for immutable Interaction source evidence.

Source-specific collectors keep cursor, dedupe, redaction and semantic workflow
ownership. This module only renders one already-redacted evidence batch into the
admitted PersonalOS `source-evidence` profile with deterministic identity.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pos_v1 import Contract


ALLOWED_EVIDENCE_KINDS = {
    "transcript",
    "message-batch",
    "source-card",
    "asset-pointer",
    "visual-context",
    "audio-transcript",
    "research",
}
ALLOWED_REDACTION_MODES = {"none", "minimized", "redacted"}


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
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a UTC offset")
    return parsed.replace(microsecond=0)


def _plain(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text or "\n" in text or "\r" in text:
        raise ValueError(f"{field} must be one non-empty line")
    return text


def _body(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} must not be empty")
    return "\n".join(line.rstrip() for line in text.splitlines())


def _json_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _validate(root: Path, path: Path, text: str) -> None:
    logical_path = path.relative_to(root).as_posix()
    failures = [
        finding
        for finding in Contract(root).validate_text(text, logical_path, resolve_relations=True)
        if finding.level == "fail"
    ]
    if failures:
        detail = "; ".join(f"{item.code}: {item.message}" for item in failures)
        raise ValueError(f"Invalid Interaction record `{logical_path}`: {detail}")


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
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


def materialize_source_evidence(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Create one deterministic, immutable source-evidence record.

    Required input keys: stable_key, channel, stream_slug, title,
    evidence_captured_at, source_system, source_ref, evidence_summary,
    source_boundary and evidence. Optional: evidence_kind, redaction_mode and
    corrections. The target Conversation Stream must already exist.
    """

    channel = _plain(record.get("channel"), "channel")
    stream_slug = _plain(record.get("stream_slug"), "stream_slug")
    if not all(part.replace("-", "").isalnum() and part == part.lower() for part in (channel, stream_slug)):
        raise ValueError("channel and stream_slug must use lower kebab case")
    captured_at = _datetime(record.get("evidence_captured_at"), "evidence_captured_at")
    stable_key = _plain(record.get("stable_key"), "stable_key")
    evidence_kind = str(record.get("evidence_kind") or "message-batch")
    redaction_mode = str(record.get("redaction_mode") or "redacted")
    if evidence_kind not in ALLOWED_EVIDENCE_KINDS:
        raise ValueError(f"Unknown evidence_kind: {evidence_kind}")
    if redaction_mode not in ALLOWED_REDACTION_MODES:
        raise ValueError(f"Unknown redaction_mode: {redaction_mode}")

    record_id = deterministic_uuid7(stable_key, captured_at)
    path = root / "interactions" / "conversations" / channel / stream_slug / "evidence" / str(captured_at.year) / f"{record_id}.md"
    interaction_ref = f"[[interactions/conversations/{channel}/{stream_slug}/conversation]]"
    title = _plain(record.get("title"), "title")
    day = captured_at.date().isoformat()
    text = "\n".join(
        [
            "---",
            "schema_version: pos-v1",
            f"id: {record_id}",
            "type: source-evidence",
            f"title: {_json_string(title)}",
            f"created: {day}",
            f"updated: {day}",
            f"evidence_kind: {evidence_kind}",
            f"evidence_captured_at: {captured_at.isoformat()}",
            f"source_system: {_json_string(_plain(record.get('source_system'), 'source_system'))}",
            f"source_ref: {_json_string(_plain(record.get('source_ref'), 'source_ref'))}",
            f"interaction_ref: {_json_string(interaction_ref)}",
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
            str(record.get("corrections") or "None.").strip(),
            "",
        ]
    )
    _validate(root, path, text)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"Source evidence identity collision: {path.relative_to(root)}")
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


def materialize_conversation_stream(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Create one deterministic Conversation Stream owner for a new source thread."""

    channel = _plain(record.get("channel"), "channel")
    stream_slug = _plain(record.get("stream_slug"), "stream_slug")
    if not all(part.replace("-", "").isalnum() and part == part.lower() for part in (channel, stream_slug)):
        raise ValueError("channel and stream_slug must use lower kebab case")
    created_at = _datetime(record.get("created_at"), "created_at")
    stable_key = _plain(record.get("stable_key"), "stable_key")
    title = _plain(record.get("title"), "title")
    participant_refs = list(dict.fromkeys(str(item).strip() for item in record.get("participant_refs", []) if str(item).strip()))
    if not participant_refs:
        raise ValueError("participant_refs must contain at least one resolving owner")
    if any(not (item.startswith("[[") and item.endswith("]]")) for item in participant_refs):
        raise ValueError("participant_refs must contain path-qualified Wikilinks")

    record_id = deterministic_uuid7(stable_key, created_at)
    path = root / "interactions" / "conversations" / channel / stream_slug / "conversation.md"
    day = created_at.date().isoformat()
    participant_yaml = json.dumps(participant_refs, ensure_ascii=False)
    current_truth = _body(record.get("current_truth"), "current_truth")
    source_gap = str(record.get("open_source_gaps") or "Keine bekannten Quellenlücken.").strip()
    text = "\n".join(
        [
            "---",
            "schema_version: pos-v1",
            f"id: {record_id}",
            "type: conversation-stream",
            f"title: {_json_string(title)}",
            f"created: {day}",
            f"updated: {day}",
            "stream_state: active",
            f"source_channel: {channel}",
            f"participant_refs: {participant_yaml}",
            "---",
            "",
            f"# {title}",
            "",
            "## Current Truth",
            "",
            current_truth,
            "",
            "## Participants",
            "",
            "\n".join(f"- {ref}" for ref in participant_refs),
            "",
            "## Coverage",
            "",
            "Der Quellenzeitraum beginnt mit dem ersten materialisierten Evidence-Record dieses Streams.",
            "",
            "## Open Source Gaps",
            "",
            source_gap,
            "",
            "## Owner Links",
            "",
            "Fachliche Wahrheit und Actions werden ausschließlich bei ihren kanonischen Ownern geführt und von Evidence-/Analysis-Records aus verlinkt.",
            "",
            "## Timeline",
            "",
            f"- **{day}** | Conversation Stream aus der stabilen Quellenidentität angelegt.",
            "",
        ]
    )
    _validate(root, path, text)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"Conversation Stream identity collision: {path.relative_to(root)}")
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
