#!/usr/bin/env python3
"""Registry-owned renderer for Automation receipts and day summaries.

Producer skills keep workflow ownership and technical cursor state. This module
only applies the shared Variant-C retention rule and materializes the admitted
PersonalOS records consistently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import fcntl

from pos_v1 import Contract, split_markdown
from time_context import resolve_timezone


MATERIAL_OUTCOMES = {
    "changed",
    "partial",
    "failed",
    "stale",
    "deferred",
    "pending",
    "external-mutation",
    "audit-no-op",
}
OPEN_OUTCOMES = {"partial", "failed", "stale", "deferred", "pending"}
ALLOWED_OUTCOMES = MATERIAL_OUTCOMES | {"no-op"}
ALLOWED_TRIGGERS = {"scheduled", "manual", "webhook", "backfill", "event"}


def deterministic_uuid7(stable_key: str, occurred_at: datetime) -> str:
    timestamp_ms = int(occurred_at.timestamp() * 1000) & ((1 << 48) - 1)
    digest = hashlib.sha256(stable_key.encode("utf-8")).digest()
    value = timestamp_ms << 80
    value |= 0x7 << 76
    value |= (int.from_bytes(digest[:2], "big") & ((1 << 12) - 1)) << 64
    value |= 0b10 << 62
    value |= int.from_bytes(digest[2:10], "big") & ((1 << 62) - 1)
    return str(uuid.UUID(int=value))


def should_retain_individual_receipt(outcome: str, retention_reason: str | None = None) -> bool:
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError(f"Unknown automation run outcome: {outcome}")
    if outcome == "audit-no-op" and not (retention_reason or "").strip():
        raise ValueError("audit-no-op requires a concrete retention_reason")
    return outcome in MATERIAL_OUTCOMES


def _datetime(value: datetime | str, field: str) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a UTC offset")
    return parsed.replace(microsecond=0)


def _json_list(values: Iterable[str]) -> str:
    return json.dumps(list(dict.fromkeys(str(item) for item in values if item)), ensure_ascii=False)


def _wikilink(path: Path, root: Path) -> str:
    return f"[[{path.relative_to(root).with_suffix('').as_posix()}]]"


def _automation_timezone(root: Path, automation_slug: str):
    record = root / "automations" / automation_slug / f"{automation_slug}.md"
    explicit = None
    if record.is_file():
        frontmatter, _keys, _body = split_markdown(record.read_text(encoding="utf-8"))
        explicit = frontmatter.get("schedule_timezone")
    return resolve_timezone(root, str(explicit) if explicit else None)


def _validate(root: Path, path: Path, text: str, *, resolve_relations: bool) -> None:
    logical_path = path.relative_to(root).as_posix()
    failures = [
        finding
        for finding in Contract(root).validate_text(text, logical_path, resolve_relations=resolve_relations)
        if finding.level == "fail"
    ]
    if failures:
        detail = "; ".join(f"{item.code}: {item.message}" for item in failures)
        raise ValueError(f"Invalid Automation record `{logical_path}`: {detail}")


def atomic_write(path: Path, text: str) -> None:
    """Write UTF-8 text durably without exposing a partially written file."""

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


def load_accounting_state(path: Path) -> dict[str, Any]:
    """Load Variant-C state; only a genuinely missing file starts empty."""

    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"retention_architecture": "variant-c-v1", "runs": []}
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Automation accounting state is unreadable: {path}") from exc
    if not isinstance(state, dict) or not isinstance(state.get("runs", []), list):
        raise ValueError(f"Automation accounting state has an invalid shape: {path}")
    return state


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Persist one JSON object through the shared atomic-write guarantee."""

    atomic_write(path, json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


@contextmanager
def accounting_lock(state_path: Path):
    """Serialize one producer's read/materialize/write accounting transaction."""

    lock_path = state_path.with_name(f".{state_path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _normalise_run(run: dict[str, Any]) -> dict[str, Any]:
    required = {"run_id", "started_at", "ended_at", "outcome", "trigger", "producer_skill_ref"}
    missing = sorted(required - set(run))
    if missing:
        raise ValueError(f"Automation accounting run is missing: {', '.join(missing)}")
    outcome = str(run["outcome"])
    reason = str(run.get("retention_reason") or "").strip() or None
    should_retain_individual_receipt(outcome, reason)
    trigger = str(run["trigger"])
    if trigger not in ALLOWED_TRIGGERS:
        raise ValueError(f"Unknown automation run trigger: {trigger}")
    started_at = _datetime(run["started_at"], "started_at")
    ended_at = _datetime(run["ended_at"], "ended_at")
    if ended_at < started_at:
        raise ValueError("ended_at must not precede started_at")
    processed_until = _datetime(run.get("processed_until", ended_at), "processed_until")
    return {
        **run,
        "run_id": str(run["run_id"]),
        "started_at": started_at,
        "ended_at": ended_at,
        "processed_until": processed_until,
        "outcome": outcome,
        "trigger": trigger,
        "retention_reason": reason,
        "affected_owner_refs": list(dict.fromkeys(run.get("affected_owner_refs") or [])),
        "evidence_refs": list(dict.fromkeys(run.get("evidence_refs") or [])),
    }


def _receipt_path(root: Path, automation_slug: str, run: dict[str, Any]) -> Path:
    local_start = run["started_at"].astimezone(_automation_timezone(root, automation_slug))
    day = local_start.date().isoformat()
    record_id = deterministic_uuid7(f"automation:{automation_slug}:run:{run['run_id']}", local_start)
    return root / "automations" / automation_slug / "receipts" / day[:4] / day / f"{record_id}.md"


def _render_receipt(root: Path, automation_slug: str, run: dict[str, Any], path: Path) -> str:
    local_timezone = _automation_timezone(root, automation_slug)
    local_start = run["started_at"].astimezone(local_timezone)
    local_end = run["ended_at"].astimezone(local_timezone)
    record_id = path.stem
    title = str(run.get("title") or f"{automation_slug} Run {run['run_id']}")
    fields = [
        "---",
        "schema_version: pos-v1",
        f"id: {record_id}",
        "type: automation-run-receipt",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"created: {local_start.date().isoformat()}",
        f"updated: {local_end.date().isoformat()}",
        f"run_id: {run['run_id']}",
        f"run_started_at: {local_start.isoformat(timespec='seconds')}",
        f"run_ended_at: {local_end.isoformat(timespec='seconds')}",
        f"run_outcome: {run['outcome']}",
        f"run_trigger: {run['trigger']}",
        f"producer_skill_ref: {json.dumps(str(run['producer_skill_ref']), ensure_ascii=False)}",
        "retention_class: material-run",
    ]
    if run["retention_reason"]:
        fields.append(f"retention_reason: {json.dumps(run['retention_reason'], ensure_ascii=False)}")
    if run["affected_owner_refs"]:
        fields.append(f"affected_owner_refs: {_json_list(run['affected_owner_refs'])}")
    if run["evidence_refs"]:
        fields.append(f"evidence_refs: {_json_list(run['evidence_refs'])}")
    fields.extend(["---", "", f"# {title}", ""])

    def section(name: str, value: str) -> None:
        fields.extend([f"## {name}", "", value.strip() or "None.", ""])

    section("Run Summary", str(run.get("summary") or f"Run `{run['run_id']}` ended with `{run['outcome']}`."))
    section(
        "Coverage",
        str(
            run.get("coverage")
            or f"Processed through {run['processed_until'].isoformat(timespec='seconds')}."
        ),
    )
    propagation = str(run.get("propagation") or "").strip()
    if not propagation and run["affected_owner_refs"]:
        propagation = "\n".join(f"- {item}" for item in run["affected_owner_refs"])
    section("Propagation", propagation or "No domain owner changed.")
    section("Errors and Pending", str(run.get("errors_pending") or "None."))
    evidence = str(run.get("evidence") or "").strip()
    if not evidence:
        evidence = "\n".join(f"- {item}" for item in run["evidence_refs"])
    section("Evidence", evidence or "Technical producer state and the linked day summary account for this run.")
    section("Corrections", "None.")
    return "\n".join(fields)


def _materialize_normalised_receipt(
    root: Path,
    automation_slug: str,
    current: dict[str, Any],
    *,
    receipt_text: str | None = None,
) -> dict[str, Any]:
    if not should_retain_individual_receipt(current["outcome"], current["retention_reason"]):
        raise ValueError("receipt-only materialization requires a material run outcome")
    receipt_path = _receipt_path(root, automation_slug, current)
    rendered = receipt_text or _render_receipt(root, automation_slug, current, receipt_path)
    _validate(root, receipt_path, rendered, resolve_relations=True)
    atomic_write(receipt_path, rendered)
    return {
        "receipt_path": receipt_path,
        "receipt_ref": _wikilink(receipt_path, root),
        "retained": True,
        "run_outcome": current["outcome"],
    }


def materialize_receipt(
    root: Path,
    automation_slug: str,
    current_run: dict[str, Any],
) -> dict[str, Any]:
    """Persist exactly one material receipt without creating a day summary.

    This narrow interface exists for self-observing backup writers such as
    ``vault-autocommit``. Their routine no-op accounting stays in external
    runtime state because a Markdown day-summary write would itself create the
    next backup mutation. All ordinary producers use :func:`materialize_run`.
    """

    if not automation_slug or any(
        char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in automation_slug
    ):
        raise ValueError("automation_slug must use lower-kebab-case")
    current = _normalise_run(current_run)
    return _materialize_normalised_receipt(root, automation_slug, current)


def _summary_outcome(runs: list[dict[str, Any]]) -> str:
    outcomes = {run["outcome"] for run in runs}
    if "failed" in outcomes:
        return "failed"
    if "stale" in outcomes:
        return "stale"
    if outcomes & {"partial", "deferred", "pending"}:
        return "partial"
    return "success"


def _day_summary_path(root: Path, automation_slug: str, day: str) -> Path:
    return root / "automations" / automation_slug / "daily" / day[:4] / f"{day}.md"


def _receipt_runs_for_day(root: Path, automation_slug: str, day: str) -> list[dict[str, Any]]:
    """Rehydrate durable material runs so a stale state cannot erase receipts."""

    receipt_dir = root / "automations" / automation_slug / "receipts" / day[:4] / day
    if not receipt_dir.is_dir():
        return []
    runs: list[dict[str, Any]] = []
    for path in sorted(receipt_dir.glob("*.md")):
        try:
            frontmatter, _keys, _body = split_markdown(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"Automation receipt cannot be reconciled: {path}") from exc
        if frontmatter.get("type") != "automation-run-receipt":
            raise ValueError(f"Unexpected record in Automation receipt directory: {path}")
        required = (
            "run_id",
            "run_started_at",
            "run_ended_at",
            "run_outcome",
            "run_trigger",
            "producer_skill_ref",
        )
        missing = [field for field in required if not frontmatter.get(field)]
        if missing:
            raise ValueError(f"Automation receipt is missing {', '.join(missing)}: {path}")
        runs.append(
            {
                "run_id": str(frontmatter["run_id"]),
                "started_at": str(frontmatter["run_started_at"]),
                "ended_at": str(frontmatter["run_ended_at"]),
                "processed_until": str(frontmatter["run_ended_at"]),
                "outcome": str(frontmatter["run_outcome"]),
                "trigger": str(frontmatter["run_trigger"]),
                "producer_skill_ref": str(frontmatter["producer_skill_ref"]),
                "retention_reason": frontmatter.get("retention_reason"),
                "affected_owner_refs": frontmatter.get("affected_owner_refs") or [],
                "evidence_refs": frontmatter.get("evidence_refs") or [],
                "receipt_ref": _wikilink(path, root),
            }
        )
    return runs


NOOP_LEDGER_RE = re.compile(
    r"^- `(?P<run_id>[^`]+)`; started=(?P<started>[^;]+); ended=(?P<ended>[^;]+); "
    r"trigger=(?P<trigger>[^;]+); producer=(?P<producer>\[\[[^\]]+\]\])$",
    re.MULTILINE,
)


def _summary_noop_runs_for_day(root: Path, automation_slug: str, day: str) -> list[dict[str, Any]]:
    """Rehydrate no-op runs from the durable aggregate ledger."""

    path = _day_summary_path(root, automation_slug, day)
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return [
        {
            "run_id": match.group("run_id"),
            "started_at": match.group("started"),
            "ended_at": match.group("ended"),
            "processed_until": match.group("ended"),
            "outcome": "no-op",
            "trigger": match.group("trigger"),
            "producer_skill_ref": match.group("producer"),
        }
        for match in NOOP_LEDGER_RE.finditer(text)
    ]


def _render_day_summary(
    root: Path,
    automation_slug: str,
    day: str,
    runs: list[dict[str, Any]],
    path: Path,
) -> str:
    local_timezone = _automation_timezone(root, automation_slug)
    local_midnight = datetime.fromisoformat(f"{day}T00:00:00").replace(tzinfo=local_timezone)
    record_id = deterministic_uuid7(f"automation:{automation_slug}:day:{day}", local_midnight)
    processed_until = max(run["processed_until"] for run in runs)
    receipt_refs = list(dict.fromkeys(run.get("receipt_ref") for run in runs if run.get("receipt_ref")))
    material_count = sum(should_retain_individual_receipt(run["outcome"], run["retention_reason"]) for run in runs)
    no_op_count = sum(run["outcome"] == "no-op" for run in runs)
    no_op_runs = [run for run in runs if run["outcome"] == "no-op"]
    open_runs = [run for run in runs if run["outcome"] in OPEN_OUTCOMES]
    owner_refs = list(
        dict.fromkeys(ref for run in runs for ref in run.get("affected_owner_refs", []))
    )
    if len(receipt_refs) != material_count:
        raise ValueError("Every material run in a day summary requires exactly one receipt_ref")
    title = f"{automation_slug} Automation Day - {day}"
    fields = [
        "---",
        "schema_version: pos-v1",
        f"id: {record_id}",
        "type: automation-day-summary",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"created: {day}",
        f"updated: {day}",
        f"day_date: {day}",
        f"timezone: {local_timezone.key}",
        f"processed_until: {processed_until.isoformat(timespec='seconds')}",
        f"producer_skill_ref: {json.dumps(str(runs[-1]['producer_skill_ref']), ensure_ascii=False)}",
        "retention_class: daily-aggregate",
        f"day_summary_outcome: {_summary_outcome(runs)}",
        "---",
        "",
        f"# {title}",
        "",
        "## Run Summary",
        "",
        f"- Abgeschlossene Runs: {len(runs)}",
        f"- Materielle Einzelbelege: {material_count}",
        f"- Routine-No-ops ohne Einzelbeleg: {no_op_count}",
        f"- Fehler oder offene Zustände: {len(open_runs)}",
        "",
        "## Coverage",
        "",
        f"- Verarbeitet bis: {processed_until.isoformat(timespec='seconds')}",
        f"- Zeitzone und Tageszuordnung: {local_timezone.key}; der Startzeitpunkt bestimmt den Lauftag.",
        "",
        "## Material Receipts",
        "",
        *(f"- {item}" for item in (receipt_refs or ["None."])),
        "",
        "## No-op Accounting",
        "",
        f"- {no_op_count} vollständig erfolgreiche Routine-No-op-Runs wurden ohne Einzelbeleg gezählt.",
        *(
            f"- `{run['run_id']}`; started={run['started_at'].isoformat(timespec='seconds')}; "
            f"ended={run['ended_at'].isoformat(timespec='seconds')}; trigger={run['trigger']}; "
            f"producer={run['producer_skill_ref']}"
            for run in no_op_runs
        ),
        "",
        "## Failures and Pending",
        "",
        *(f"- `{run['run_id']}`: {run['outcome']}" for run in (open_runs or [{"run_id": "none", "outcome": "None."}])),
        "",
        "## Propagation",
        "",
        *(f"- {item}" for item in (owner_refs or ["No domain owner changed."])),
        "",
        "## Corrections",
        "",
        "None.",
        "",
    ]
    return "\n".join(fields)


def _materialize_day_summary(
    root: Path,
    automation_slug: str,
    current: dict[str, Any],
    runs: Iterable[dict[str, Any]],
) -> Path:
    local_timezone = _automation_timezone(root, automation_slug)
    day = current["started_at"].astimezone(local_timezone).date().isoformat()
    day_runs = [
        normalised
        for item in runs
        for normalised in [_normalise_run(item)]
        if normalised["started_at"].astimezone(local_timezone).date().isoformat() == day
    ]
    day_runs.sort(key=lambda run: (run["started_at"], run["run_id"]))
    day_path = _day_summary_path(root, automation_slug, day)
    day_text = _render_day_summary(root, automation_slug, day, day_runs, day_path)
    _validate(root, day_path, day_text, resolve_relations=True)
    atomic_write(day_path, day_text)
    return day_path


def materialize_run(
    root: Path,
    automation_slug: str,
    current_run: dict[str, Any],
    *,
    accounted_runs: Iterable[dict[str, Any]] = (),
    receipt_text: str | None = None,
) -> dict[str, Any]:
    """Persist the current receipt when required and rebuild its day summary.

    ``accounted_runs`` must come from the producer's technical state and include
    only runs already closed under this retention architecture. The current run
    is merged by ``run_id``, so retries are idempotent.
    """

    if not automation_slug or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in automation_slug):
        raise ValueError("automation_slug must use lower-kebab-case")
    current = _normalise_run(current_run)
    merged: dict[str, dict[str, Any]] = {
        normalised["run_id"]: normalised
        for item in accounted_runs
        for normalised in [_normalise_run(item)]
    }
    merged[current["run_id"]] = current

    local_timezone = _automation_timezone(root, automation_slug)
    day = current["started_at"].astimezone(local_timezone).date().isoformat()
    for durable in [
        *_receipt_runs_for_day(root, automation_slug, day),
        *_summary_noop_runs_for_day(root, automation_slug, day),
    ]:
        merged.setdefault(durable["run_id"], _normalise_run(durable))

    receipt_path: Path | None = None
    if should_retain_individual_receipt(current["outcome"], current["retention_reason"]):
        receipt = _materialize_normalised_receipt(
            root,
            automation_slug,
            current,
            receipt_text=receipt_text,
        )
        receipt_path = receipt["receipt_path"]
        current["receipt_ref"] = receipt["receipt_ref"]
        merged[current["run_id"]] = current

    day_path = _materialize_day_summary(root, automation_slug, current, merged.values())
    return {
        "receipt_path": receipt_path,
        "receipt_ref": current.get("receipt_ref"),
        "day_summary_path": day_path,
        "day_summary_ref": _wikilink(day_path, root),
        "retained": receipt_path is not None,
        "run_outcome": current["outcome"],
    }


def materialize_accounted_run(
    root: Path,
    automation_slug: str,
    current_run: dict[str, Any],
    state_path: Path,
    *,
    max_runs: int = 100,
    receipt_text: str | None = None,
) -> dict[str, Any]:
    """Materialize a producer run and update its external accounting state."""

    if max_runs < 1:
        raise ValueError("max_runs must be positive")
    with accounting_lock(state_path):
        current = _normalise_run(current_run)
        local_timezone = _automation_timezone(root, automation_slug)
        day = current["started_at"].astimezone(local_timezone).date().isoformat()
        if not state_path.exists() and _day_summary_path(root, automation_slug, day).exists():
            raise ValueError(
                "Automation accounting state is missing while a day summary already exists; "
                "restore or reconcile the state before another write"
            )
        state = load_accounting_state(state_path)
        run_id = str(current_run.get("run_id") or "")
        prior_by_id = {
            str(run.get("run_id")): run
            for run in state.get("runs", [])
            if str(run.get("run_id")) != run_id
        }
        for durable in _receipt_runs_for_day(root, automation_slug, day):
            if durable["run_id"] != run_id:
                prior_by_id[durable["run_id"]] = durable
        for durable in _summary_noop_runs_for_day(root, automation_slug, day):
            if durable["run_id"] != run_id:
                prior_by_id[durable["run_id"]] = durable
        prior = list(prior_by_id.values())
        receipt_path: Path | None = None
        receipt_ref: str | None = None
        if should_retain_individual_receipt(current["outcome"], current["retention_reason"]):
            receipt = _materialize_normalised_receipt(
                root,
                automation_slug,
                current,
                receipt_text=receipt_text,
            )
            receipt_path = receipt["receipt_path"]
            receipt_ref = receipt["receipt_ref"]
            current["receipt_ref"] = receipt_ref

        persisted = dict(current)
        for field in ("started_at", "ended_at", "processed_until"):
            persisted[field] = persisted[field].isoformat(timespec="seconds")
        if receipt_ref:
            persisted["receipt_ref"] = receipt_ref
        runs = [*prior, persisted]
        runs.sort(key=lambda run: (str(run.get("started_at")), str(run.get("run_id"))))
        current_day_runs = [
            run
            for run in runs
            if _datetime(run["started_at"], "started_at").astimezone(local_timezone).date().isoformat() == day
        ]
        older_runs = [run for run in runs if run not in current_day_runs]
        retained_runs = [*older_runs[-max_runs:], *current_day_runs]
        state.update(
            {
                "retention_architecture": "variant-c-v1",
                "updated_at": persisted["ended_at"],
                "runs": retained_runs,
            }
        )
        atomic_write_json(state_path, state)
        day_path = _materialize_day_summary(
            root,
            automation_slug,
            current,
            retained_runs,
        )
        return {
            "receipt_path": receipt_path,
            "receipt_ref": receipt_ref,
            "day_summary_path": day_path,
            "day_summary_ref": _wikilink(day_path, root),
            "retained": receipt_path is not None,
            "run_outcome": current["outcome"],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["account-run"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--automation", required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Input must be one JSON object")
    result = materialize_accounted_run(
        args.root,
        args.automation,
        payload,
        args.state,
    )
    serialisable = {
        key: str(value) if isinstance(value, Path) else value
        for key, value in result.items()
    }
    print(json.dumps(serialisable, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
