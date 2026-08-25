#!/usr/bin/env python3
"""Build the bounded PersonalOS priority dashboard from canonical records."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable


OPEN_ACTION_LIFECYCLES = {"ready", "in-progress", "waiting", "blocked", "deferred"}
CLOSED_ACTION_LIFECYCLES = {"completed", "cancelled"}
TERMINAL_TRIGGER_LIFECYCLES = {"resolved", "cancelled"}
OPPORTUNITY_PHASES = {"discovery", "proposal", "nurture", "lead", "revalidation"}
PRIORITY_WEIGHT = {"critical": 0, "high": 1, "normal": 2, "low": 3, None: 4}
SOURCE_DIGEST_RE = re.compile(r"Source-Digest `([0-9a-f]{64})`")


def load_runtime(base: Path):
    runtime_path = base / "system/data-model/scripts/pos_v1.py"
    spec = importlib.util.spec_from_file_location("priority_dashboard_pos_v1_runtime", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load pos-v1 runtime: {runtime_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def section(body: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    text = match.group(1).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def compact(text: str, limit: int = 240) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip(" ,.;:") + "…"


def ref_target(value: str) -> str:
    inner = value[2:-2]
    return inner.split("|", 1)[0].split("#", 1)[0].strip()


def canonical_ref(path: Path, base: Path) -> str:
    return path.relative_to(base).with_suffix("").as_posix()


@dataclass
class OwnerContext:
    ref: str
    title: str
    lifecycle: str | None
    priority: str | None
    commercial_state: str | None
    project_phase: str | None
    workflow: str | None = None

    @property
    def is_opportunity(self) -> bool:
        return self.commercial_state == "open" and self.project_phase in OPPORTUNITY_PHASES

    @property
    def impact_weight(self) -> int:
        if self.lifecycle == "active" and self.priority == "critical":
            return 0
        if self.lifecycle == "active" and self.priority == "high":
            return 1
        if self.lifecycle == "active" and self.commercial_state == "won":
            return 2
        if self.lifecycle == "active":
            return 3
        return 4


@dataclass
class Action:
    path: Path
    ref: str
    title: str
    lifecycle: str
    action_priority: str | None
    due: date | None
    target: date | None
    not_before: date | None
    follow_up_at: date | None
    updated: date
    next_action: str
    desired_outcome: str
    current_truth: str
    affected_refs: list[str] = field(default_factory=list)
    owner_contexts: list[OwnerContext] = field(default_factory=list)

    @property
    def personal_change(self) -> bool:
        return any(owner.workflow == "personal-change" for owner in self.owner_contexts)

    @property
    def admin_related(self) -> bool:
        has_finance_owner = any(ref.startswith("finance/") for ref in self.affected_refs)
        has_project_owner = bool(self.owner_contexts)
        return has_finance_owner and not has_project_owner

    @property
    def opportunity_only(self) -> bool:
        return bool(self.owner_contexts) and all(owner.is_opportunity for owner in self.owner_contexts)

    @property
    def best_owner(self) -> OwnerContext | None:
        if not self.owner_contexts:
            return None
        return sorted(self.owner_contexts, key=lambda owner: (owner.impact_weight, owner.title.casefold()))[0]

    def effective_date(self) -> date | None:
        values = [value for value in (self.due, self.target) if value is not None]
        return min(values) if values else None


@dataclass
class Trigger:
    path: Path
    ref: str
    title: str
    lifecycle: str
    review_at: date
    reassessment: str


@dataclass
class Control:
    lifecycle: str = "inactive"
    review_on: date | None = None
    expires_on: date | None = None
    focus_areas: list[str] = field(default_factory=list)
    focus_refs: list[str] = field(default_factory=list)
    ordered_refs: list[str] = field(default_factory=list)
    excluded_refs: list[str] = field(default_factory=list)

    def effective(self, today: date) -> bool:
        return self.lifecycle == "active" and self.expires_on is not None and today <= self.expires_on

    def expired(self, today: date) -> bool:
        return self.lifecycle == "active" and self.expires_on is not None and today > self.expires_on


@dataclass
class DashboardSelection:
    today: list[Action]
    week: list[Action]
    life_horizon: list[Action]
    waiting_actions: list[Action]
    due_triggers: list[Trigger]
    admin_actions: list[Action]
    urgent_not_focus: list[Action]
    warnings: list[str]


def markdown_index(base: Path) -> tuple[dict[str, Path], dict[str, list[Path]]]:
    direct: dict[str, Path] = {}
    basenames: dict[str, list[Path]] = {}
    for path in base.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel = canonical_ref(path, base)
        direct[rel] = path
        basenames.setdefault(path.stem, []).append(path)
    return direct, basenames


def resolve_ref(target: str, direct: dict[str, Path], basenames: dict[str, list[Path]]) -> Path | None:
    normalized = target[:-3] if target.endswith(".md") else target
    if normalized in direct:
        return direct[normalized]
    matches = basenames.get(Path(normalized).name, [])
    return matches[0] if len(matches) == 1 else None


def load_owner_contexts(
    refs: Iterable[str],
    base: Path,
    runtime,
    direct: dict[str, Path],
    basenames: dict[str, list[Path]],
) -> list[OwnerContext]:
    owners: list[OwnerContext] = []
    for raw in refs:
        if not isinstance(raw, str) or not raw.startswith("[["):
            continue
        target = ref_target(raw)
        path = resolve_ref(target, direct, basenames)
        if path is None:
            continue
        try:
            fm, _, _ = runtime.split_markdown(path.read_text(encoding="utf-8"))
        except (OSError, runtime.ContractError):
            continue
        if fm.get("type") != "project":
            continue
        owners.append(
            OwnerContext(
                ref=canonical_ref(path, base),
                title=str(fm.get("title", path.stem)),
                lifecycle=fm.get("lifecycle"),
                priority=fm.get("priority"),
                commercial_state=fm.get("commercial_state"),
                project_phase=fm.get("project_phase"),
                workflow=fm.get("workflow"),
            )
        )
    return owners


def load_actions(base: Path, runtime) -> list[Action]:
    direct, basenames = markdown_index(base)
    actions: list[Action] = []
    for path in sorted((base / "operations/actions").glob("*.md")):
        if path.name == "index.md":
            continue
        fm, _, body = runtime.split_markdown(path.read_text(encoding="utf-8"))
        if fm.get("type") != "action":
            raise RuntimeError(f"Non-Action record in operations/actions: {path}")
        lifecycle = fm.get("lifecycle")
        if lifecycle in CLOSED_ACTION_LIFECYCLES:
            continue
        if lifecycle not in OPEN_ACTION_LIFECYCLES:
            raise RuntimeError(f"Unknown Action lifecycle `{lifecycle}`: {path}")
        updated = parse_date(fm.get("updated"))
        if updated is None:
            raise RuntimeError(f"Action has invalid updated date: {path}")
        owner_refs = fm.get("affected_owner_refs", [])
        affected_refs = [
            ref_target(value)
            for value in owner_refs
            if isinstance(value, str) and value.startswith("[[") and value.endswith("]]")
        ]
        actions.append(
            Action(
                path=path,
                ref=canonical_ref(path, base),
                title=str(fm.get("title", path.stem)),
                lifecycle=str(lifecycle),
                action_priority=fm.get("action_priority"),
                due=parse_date(fm.get("due")),
                target=parse_date(fm.get("target")),
                not_before=parse_date(fm.get("not_before")),
                follow_up_at=parse_date(fm.get("follow_up_at")),
                updated=updated,
                next_action=section(body, "Next Action"),
                desired_outcome=section(body, "Desired Outcome"),
                current_truth=section(body, "Current Truth"),
                affected_refs=affected_refs,
                owner_contexts=load_owner_contexts(owner_refs, base, runtime, direct, basenames),
            )
        )
    return actions


def load_triggers(base: Path, runtime) -> list[Trigger]:
    triggers: list[Trigger] = []
    for path in sorted((base / "operations/attention-triggers").glob("*.md")):
        if path.name == "index.md":
            continue
        fm, _, body = runtime.split_markdown(path.read_text(encoding="utf-8"))
        if fm.get("type") != "attention-trigger" or fm.get("lifecycle") in TERMINAL_TRIGGER_LIFECYCLES:
            continue
        review_at = parse_date(fm.get("review_at"))
        if review_at is None:
            raise RuntimeError(f"Attention Trigger has invalid review_at: {path}")
        triggers.append(
            Trigger(
                path=path,
                ref=canonical_ref(path, base),
                title=str(fm.get("title", path.stem)),
                lifecycle=str(fm.get("lifecycle")),
                review_at=review_at,
                reassessment=section(body, "Reassessment Rule"),
            )
        )
    return triggers


def load_control(base: Path, runtime) -> Control:
    path = base / "operations/priority-control.md"
    if not path.is_file():
        return Control()
    fm, _, _ = runtime.split_markdown(path.read_text(encoding="utf-8"))
    if fm.get("type") != "priority-control":
        raise RuntimeError("operations/priority-control.md is not a priority-control record")
    return Control(
        lifecycle=str(fm.get("lifecycle", "inactive")),
        review_on=parse_date(fm.get("priority_control_review_on")),
        expires_on=parse_date(fm.get("priority_control_expires_on")),
        focus_areas=[str(value) for value in fm.get("priority_focus_areas", [])],
        focus_refs=[ref_target(value) for value in fm.get("priority_focus_action_refs", [])],
        ordered_refs=[ref_target(value) for value in fm.get("priority_ordered_action_refs", [])],
        excluded_refs=[ref_target(value) for value in fm.get("priority_excluded_action_refs", [])],
    )


def action_rank(action: Action, today: date, horizon_end: date, control: Control) -> tuple:
    manual_focus = control.focus_refs.index(action.ref) if action.ref in control.focus_refs else 10_000
    manual_order = control.ordered_refs.index(action.ref) if action.ref in control.ordered_refs else 10_000
    if manual_focus < 10_000:
        tier = 0
    elif action.due == today:
        tier = 10
    elif action.due is not None and action.due < today:
        tier = 12
    elif action.due is not None and action.due <= horizon_end:
        tier = 20
    elif action.action_priority == "critical":
        tier = 30
    elif action.lifecycle == "in-progress":
        tier = 31
    elif action.action_priority == "high":
        tier = 32
    elif action.best_owner is not None and not action.opportunity_only:
        tier = 40 + action.best_owner.impact_weight
    elif action.opportunity_only:
        tier = 60
    else:
        tier = 50

    if action.due is None:
        due_weight = date.max.toordinal()
    elif action.due < today:
        due_weight = -action.due.toordinal()
    else:
        due_weight = action.due.toordinal()
    if action.target is None or action.target < today:
        target_weight = date.max.toordinal()
    else:
        target_weight = action.target.toordinal()
    lifecycle_weight = 0 if action.lifecycle == "in-progress" else 1
    return (
        manual_focus,
        manual_order,
        tier,
        due_weight,
        PRIORITY_WEIGHT.get(action.action_priority, 4),
        lifecycle_weight,
        target_weight,
        -action.updated.toordinal(),
        action.title.casefold(),
    )


def stale_overdue(action: Action, today: date) -> bool:
    effective = action.effective_date()
    if effective is None or effective >= today - timedelta(days=3):
        return False
    return True


def waiting_risk_weight(action: Action) -> int:
    if any(ref.startswith("finance/") for ref in action.affected_refs):
        return 0
    if action.best_owner is not None and action.best_owner.workflow == "delivery":
        return 0
    if action.best_owner is not None and action.best_owner.is_opportunity:
        return 1
    return 2


def month_end_batch_window(today: date) -> bool:
    next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
    month_end = next_month - timedelta(days=1)
    return today >= month_end - timedelta(days=4)


def select(actions: list[Action], triggers: list[Trigger], control: Control, today: date) -> DashboardSelection:
    horizon_end = today + timedelta(days=6)
    month_end = today + timedelta(days=30)
    warnings: list[str] = []
    effective_control = control if control.effective(today) else Control()
    known = {action.ref for action in actions}
    if control.effective(today):
        conflicts = set(control.excluded_refs) & (set(control.focus_refs) | set(control.ordered_refs))
        if conflicts:
            raise RuntimeError(f"Priority Control includes and excludes the same Action refs: {sorted(conflicts)}")
        unknown = (set(control.focus_refs) | set(control.ordered_refs) | set(control.excluded_refs)) - known
        warnings.extend(f"Unbekannter Control-Link: [[{ref}]]" for ref in sorted(unknown))
    visible = [action for action in actions if action.ref not in set(effective_control.excluded_refs)]
    executable = [
        action
        for action in visible
        if action.lifecycle not in {"waiting", "blocked"}
        and not (action.lifecycle == "deferred" and action.not_before is not None and action.not_before > today)
    ]
    manual_refs = set(effective_control.focus_refs) | set(effective_control.ordered_refs)
    admin_pool = [
        action
        for action in executable
        if action.admin_related and action.ref not in manual_refs and action.action_priority != "critical"
    ]
    main_executable = [action for action in executable if action not in admin_pool]
    ranked = sorted(main_executable, key=lambda item: action_rank(item, today, horizon_end, effective_control))

    current_candidates = [action for action in ranked if action.ref in effective_control.focus_refs]
    if not current_candidates:
        current_candidates = [
            action
            for action in ranked
            if not stale_overdue(action, today)
            and (
                (action.due is not None and action.due <= today)
                or action.lifecycle == "in-progress"
                or action.action_priority == "critical"
            )
        ]
    if not current_candidates:
        current_candidates = [action for action in ranked if not stale_overdue(action, today)]
    today_items = current_candidates[:1]

    selected_refs = {action.ref for action in today_items}
    week_items: list[Action] = []
    for action in ranked:
        if action.ref in selected_refs:
            continue
        manual = action.ref in manual_refs
        week_relevant = (
            manual
            or (action.due is not None and action.due <= horizon_end)
            or (action.target is not None and today <= action.target <= horizon_end)
            or action.lifecycle == "in-progress"
            or (action.best_owner is not None and action.best_owner.impact_weight <= 2)
            or action.action_priority in {"critical", "high"}
        )
        if week_relevant and (manual or not stale_overdue(action, today)):
            week_items.append(action)
            selected_refs.add(action.ref)
        if len(week_items) == 3:
            break

    life_limit = min(2, max(0, 5 - len(today_items) - len(week_items)))
    life_horizon: list[Action] = []
    for action in ranked:
        if action.ref in selected_refs or not action.personal_change or stale_overdue(action, today):
            continue
        horizon_date = action.due or action.target
        if (
            (horizon_date is not None and horizon_date <= month_end)
            or action.action_priority in {"critical", "high"}
            or action.lifecycle == "in-progress"
        ):
            life_horizon.append(action)
            selected_refs.add(action.ref)
        if len(life_horizon) == life_limit:
            break

    waiting_actions = sorted(
        [
            action
            for action in visible
            if action.lifecycle == "waiting"
            and (
                (action.follow_up_at is not None and action.follow_up_at <= horizon_end)
                or (action.due is not None and action.due <= horizon_end)
                or (
                    action.action_priority in {"critical", "high"}
                    and action.follow_up_at is not None
                    and action.follow_up_at <= month_end
                )
                or (
                    action.best_owner is not None
                    and action.best_owner.workflow == "delivery"
                    and action.follow_up_at is not None
                    and action.follow_up_at <= month_end
                )
            )
        ],
        key=lambda item: (
            waiting_risk_weight(item),
            PRIORITY_WEIGHT.get(item.action_priority, 4),
            item.follow_up_at or item.due or date.max,
            item.title.casefold(),
        ),
    )
    due_triggers = sorted(
        [trigger for trigger in triggers if trigger.lifecycle == "due" or trigger.review_at <= today],
        key=lambda item: (item.review_at, item.title.casefold()),
    )
    trigger_limit = min(2, len(due_triggers))
    waiting_limit = 5 - trigger_limit
    waiting_actions = waiting_actions[:waiting_limit]
    due_triggers = due_triggers[:trigger_limit]

    admin_actions: list[Action] = []
    if month_end_batch_window(today):
        admin_actions = sorted(
            [action for action in admin_pool if action.ref not in selected_refs],
            key=lambda item: action_rank(item, today, horizon_end, effective_control),
        )[:3]

    urgent_not_focus = sorted(
        [
            action
            for action in visible
            if action.ref not in selected_refs
            and action.lifecycle != "waiting"
            and action not in admin_pool
            and (
                stale_overdue(action, today)
                or (action.due is not None and action.due <= horizon_end)
                or action.action_priority == "critical"
            )
        ],
        key=lambda item: action_rank(item, today, horizon_end, effective_control),
    )[:5]

    return DashboardSelection(
        today=today_items,
        week=week_items,
        life_horizon=life_horizon,
        waiting_actions=waiting_actions,
        due_triggers=due_triggers,
        admin_actions=admin_actions,
        urgent_not_focus=urgent_not_focus,
        warnings=warnings,
    )


def why(action: Action, today: date, horizon_end: date, control: Control) -> str:
    reasons: list[str] = []
    if control.effective(today) and action.ref in control.focus_refs:
        reasons.append(f"MANUELLER OVERRIDE bis {control.expires_on.isoformat()}")
    if action.due is not None:
        if action.due < today:
            reasons.append(f"echte Deadline seit {action.due.isoformat()} überfällig")
        elif action.due == today:
            reasons.append("heute fällig")
        elif action.due <= horizon_end:
            reasons.append(f"in den nächsten sieben Tagen fällig ({action.due.isoformat()})")
    elif action.target is not None:
        if action.target < today:
            reasons.append(f"weiches Planungsziel {action.target.isoformat()} überschritten; Review statt Deadline")
        elif action.target <= horizon_end:
            reasons.append(f"weiches Sieben-Tage-Planungsziel {action.target.isoformat()}")
    owner = action.best_owner
    if owner is not None:
        if owner.is_opportunity:
            reasons.append(f"Opportunity nach festen Commitments: [[{owner.ref}|{owner.title}]]")
        elif owner.lifecycle == "active" and owner.priority in {"critical", "high"}:
            reasons.append(f"aktives {owner.priority}-Project [[{owner.ref}|{owner.title}]]")
        elif owner.lifecycle == "active" and owner.commercial_state == "won":
            reasons.append(f"gewonnenes aktives Project [[{owner.ref}|{owner.title}]]")
    if action.lifecycle == "in-progress":
        reasons.append("bereits in Arbeit")
    if action.action_priority in {"critical", "high"} and not reasons:
        reasons.append(f"kanonische Action-Priorität {action.action_priority}")
    return "; ".join(reasons[:2]) or "offenes bestätigtes Commitment mit aktuellem Next Action"


def action_line(action: Action, detail: str, reason: str) -> list[str]:
    label = compact(action.title, 110)
    lines = [f"- **[[{action.ref}|{label}]]** — **Warum:** {reason}."]
    if detail:
        lines.append(f"  - {detail}")
    return lines


def focus_areas(selection: DashboardSelection, control: Control, today: date) -> list[str]:
    if control.effective(today) and control.focus_areas:
        return control.focus_areas[:3]
    result: list[str] = []
    for action in [*selection.today, *selection.week, *selection.life_horizon]:
        owner = action.best_owner
        lowered = action.title.casefold()
        if any(token in lowered for token in ("rechnung", "lexware", "zahlung", "abo", "finance")):
            candidate = "Finance und Admin"
        elif any(token in lowered for token in ("antworte", "termin", "kommuniziere", "telefonier", "rückmeldung")):
            candidate = "Kommunikation und Termine"
        elif any(token in lowered for token in ("video", "content", "newsletter", "upload")):
            candidate = "Content"
        elif any(token in lowered for token in ("personalo", "system", "automation", "dashboard")):
            candidate = "Systemarbeit"
        elif any(token in lowered for token in ("bali", "reise", "visum", "wohnung")):
            candidate = "Bali-Vorbereitung"
        else:
            candidate = owner.title if owner is not None else "Operative Commitments"
        if candidate not in result:
            result.append(candidate)
        if len(result) == 3:
            break
    return result


def source_digest(base: Path) -> str:
    paths = [
        base / "skills/priority-dashboard/scripts/rebuild.py",
        base / "skills/priority-dashboard/SKILL.md",
        base / "system/frameworks/operations/priority-dashboard.md",
        *sorted((base / "operations/actions").glob("*.md")),
        *sorted((base / "operations/attention-triggers").glob("*.md")),
        base / "operations/priority-control.md",
        *sorted((base / "projects").glob("*/*.md")),
    ]
    digest = hashlib.sha256()
    for path in paths:
        if not path.is_file() or path.name == "index.md":
            continue
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def saved_source_digest(text: str) -> str | None:
    match = SOURCE_DIGEST_RE.search(text)
    return match.group(1) if match else None


def render_dashboard(
    base: Path,
    runtime,
    selection: DashboardSelection,
    control: Control,
    now: datetime,
    reason: str,
) -> str:
    today = now.date()
    horizon_end = today + timedelta(days=6)
    month_end = today + timedelta(days=30)
    path = base / "operations/priority-dashboard.md"
    record_id = "01a0251c-9ee7-7315-a87d-b8c885d2ca93"
    created = "2026-08-21"
    if path.is_file():
        existing, _, _ = runtime.split_markdown(path.read_text(encoding="utf-8"))
        record_id = str(existing.get("id", record_id))
        created = str(existing.get("created", created))
    timestamp = now.isoformat(timespec="seconds")
    digest = source_digest(base)
    areas = focus_areas(selection, control, today)
    effective_control = control if control.effective(today) else Control()

    lines = [
        "---",
        "schema_version: pos-v1",
        f"id: {record_id}",
        "type: view-record",
        'title: "Priority Dashboard"',
        f"created: {created}",
        f"updated: {today.isoformat()}",
        "lifecycle: active",
        'canonical_system_ref: "[[system/truth-systems/personalos]]"',
        "authority_scope: pointer",
        "view_kind: dashboard",
        "derivation_mode: generated",
        'source_owner_refs: ["index", "index", "priority control"]',
        "---",
        "",
        "# Priority Dashboard",
        "",
        "## Purpose",
        "",
        "Morgentaugliche, dynamische Prioritätssicht über kanonische Actions, Attention Trigger und relevante Owner. Diese Datei ist kein Task-Speicher: Sie besitzt keine Checkboxen, keine unabhängige Completion und keinen eigenen Action-Lifecycle.",
        "",
        "## Source Owners",
        "",
        "Kanonische Ausführungswahrheit: index. Neubewertung ohne aktuelle Action: index. Temporäre manuelle Richtung: priority control. Project-, Domain-, Deadline- und Evidenzwahrheit verbleibt bei den jeweils verlinkten Ownern.",
        "",
        "## Derivation",
        "",
        "Automatische Präzedenz: wirksame explizite Overrides → echte Deadlines/Zusagen im rollierenden Sieben-Tage-Fenster → explizite Critical-/High-Priorität und tatsächlich laufende Arbeit → Project-Impact → weiche Targets als Tie-Breaker → Opportunities. Freitext-Cadences beeinflussen das Ranking nicht.",
        "",
        "### Manueller Control",
        "",
    ]
    if control.effective(today):
        areas_text = ", ".join(control.focus_areas) if control.focus_areas else "nur verlinkte Action-Steuerung"
        lines.append(
            f"**MANUELLER OVERRIDE — wirksam bis {control.expires_on.isoformat()}** · Review {control.review_on.isoformat() if control.review_on else 'nicht gesetzt'} · Fokus: {areas_text}. Diese Richtung schlägt automatische Empfehlungen."
        )
    elif control.expired(today):
        lines.append(
            f"**ABGELAUFENER MANUELLER OVERRIDE — automatisch ignoriert seit {control.expires_on.isoformat()}**. Keine automatische Verlängerung; priority control prüfen."
        )
    else:
        lines.append("Kein manueller Override aktiv. Die folgenden Punkte sind generierte Empfehlungen.")
    lines.extend(["", "### Aktueller Fokus", ""])
    if areas:
        lines.append("**Fokusfelder:** " + " · ".join(areas))
        lines.append("")
    if selection.today:
        for action in selection.today:
            lines.extend(action_line(action, "Nächster Schritt: " + compact(action.next_action), why(action, today, horizon_end, effective_control)))
    else:
        lines.append("- Keine belastbare aktuelle Fokus-Action aus den kanonischen Records ableitbar.")

    lines.extend(["", "### Nächste sieben Tage", ""])
    if selection.week:
        for action in selection.week:
            detail = "Outcome: " + compact(action.desired_outcome or action.next_action)
            lines.extend(action_line(action, detail, why(action, today, horizon_end, effective_control)))
    else:
        lines.append(f"- Keine zusätzliche Action im rollierenden Fenster bis {horizon_end.isoformat()}.")

    lines.extend(["", "### 30-Tage-Lebens- und Reisegates", ""])
    if selection.life_horizon:
        for action in selection.life_horizon:
            detail = "Outcome: " + compact(action.desired_outcome or action.next_action)
            lines.extend(action_line(action, detail, why(action, today, month_end, effective_control)))
    else:
        lines.append(f"- Kein zusätzliches persönliches Gate bis {month_end.isoformat()} außerhalb des Hauptfokus.")

    lines.extend(["", "### Kunden-, Cashflow- und Waiting-Risiken", ""])
    if selection.waiting_actions or selection.due_triggers:
        for action in selection.waiting_actions:
            boundary = action.follow_up_at or action.due
            reason_text = f"externes Waiting/Risiko; Follow-up {boundary.isoformat() if boundary else 'ohne Datum'}"
            lines.extend(action_line(action, "Nächster Prüfpunkt: " + compact(action.next_action), reason_text))
        for trigger in selection.due_triggers:
            lines.append(
                f"- **[[{trigger.ref}|{compact(trigger.title, 110)}]]** — **Warum:** Neubewertung seit {trigger.review_at.isoformat()} fällig."
            )
            if trigger.reassessment:
                lines.append(f"  - Reassessment: {compact(trigger.reassessment)}")
    else:
        lines.append("- Keine im relevanten Horizont fällige externe Rückmeldung, Cashflow-Prüfung oder Neubewertung.")

    lines.extend(["", "### Admin-Batch", ""])
    if selection.admin_actions:
        for action in selection.admin_actions:
            lines.extend(action_line(action, "Admin-Nächster Schritt: " + compact(action.next_action), "gebündelte Finance-/Admin-Arbeit; kein automatischer Deep-Work-Fokus"))
    else:
        lines.append("- Routinebelege werden gesammelt und erst im Monatsendfenster als gemeinsamer Buchungs-Batch eingeblendet.")

    lines.extend(["", "### Stale Review", ""])
    if selection.urgent_not_focus:
        for action in selection.urgent_not_focus:
            base_reason = why(action, today, horizon_end, effective_control)
            if stale_overdue(action, today):
                base_reason += "; alten Record bestätigen, schließen oder realistisch neu planen"
            lines.extend(action_line(action, "Bewusst außerhalb des Hauptfokus; zuerst Wahrheit und Timing prüfen.", base_reason))
    else:
        lines.append("- Keine zusätzliche stale oder dringende Action außerhalb des Hauptfokus.")
    if selection.warnings:
        lines.extend(["", "### Control-Hinweise", ""])
        lines.extend(f"- {warning}" for warning in selection.warnings)
    lines.extend(
        [
            "",
            "## Freshness",
            "",
            f"Generiert am `{timestamp}` · Zeitzone `{now.tzinfo}` · Rebuild-Grund `{reason}` · Source-Digest `{digest}`.",
            "",
            "Expliziter Refresh nach Prioritätsänderung: `python3 skills/priority-dashboard/scripts/rebuild.py --reason manual-priority-change`. Nach Action-/Trigger-/Owner-Änderung: derselbe Befehl mit `--reason operational-state-change`. Zusätzlich läuft täglich ein Service-Host-Rebuild vor 06:00; es gibt keinen Realtime-Watcher.",
            "",
            "## Limitations",
            "",
            "Die Sicht kann nur vorhandene, aktuelle kanonische Records priorisieren. Ideen, Freitext-Cadences oder vermutete Arbeit werden nicht in Actions umgedeutet. `due` bleibt eine echte Frist; `target` ist nur ein weiches Planungsdatum und erzeugt allein keinen Fokus. Kalendertermine begrenzen reale Kapazität, werden hier aber nicht als zweite Taskliste gespiegelt. Alte überfällige Actions bleiben im Stale Review sichtbar. Änderungen an Completion, Lifecycle, Deadline oder Project State erfolgen ausschließlich beim jeweiligen Owner.",
            "",
        ]
    )
    text = "\n".join(lines)
    if "- [ ]" in text or "- [x]" in text.lower():
        raise RuntimeError("Rendered dashboard contains forbidden checkboxes")
    main_refs = {action.ref for action in [*selection.today, *selection.week, *selection.life_horizon]}
    if len(main_refs) > 5:
        raise RuntimeError("Rendered dashboard exceeds five main-focus Action links")
    return text


def resolve_now(base: Path, runtime, explicit_timezone: str | None, as_of: str | None) -> datetime:
    time_module_path = base / "system/data-model/scripts/time_context.py"
    spec = importlib.util.spec_from_file_location("priority_dashboard_time_context", time_module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load time context resolver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    timezone = module.resolve_timezone(base, explicit_timezone)
    if as_of:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of):
            return datetime.fromisoformat(as_of + "T05:40:00").replace(tzinfo=timezone)
        parsed = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone)
        return parsed.astimezone(timezone)
    return datetime.now(timezone)


def build(base: Path, reason: str, timezone: str | None, as_of: str | None) -> tuple[str, DashboardSelection, Control]:
    runtime = load_runtime(base)
    now = resolve_now(base, runtime, timezone, as_of)
    actions = load_actions(base, runtime)
    triggers = load_triggers(base, runtime)
    control = load_control(base, runtime)
    selection = select(actions, triggers, control, now.date())
    rendered = render_dashboard(base, runtime, selection, control, now, reason)
    findings = runtime.Contract(base).validate_text(rendered, "operations/priority-dashboard.md", resolve_relations=True)
    failures = [finding for finding in findings if finding.level == "fail"]
    if failures:
        detail = "; ".join(f"{item.code}: {item.message}" for item in failures)
        raise RuntimeError(f"Rendered dashboard failed pos-v1 validation: {detail}")
    return rendered, selection, control


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument(
        "--reason",
        choices=["scheduled", "manual", "manual-priority-change", "operational-state-change"],
        default="manual",
    )
    parser.add_argument("--timezone", default=None)
    parser.add_argument("--as-of", default=None, help="Testing override: YYYY-MM-DD or RFC3339")
    parser.add_argument("--check", action="store_true", help="Fail when the saved dashboard is invalid or its source digest is stale; do not write")
    args = parser.parse_args()
    base = args.base.resolve()
    output = base / "operations/priority-dashboard.md"
    try:
        if args.check:
            if not output.is_file():
                print("priority-dashboard: drift")
                return 1
            runtime = load_runtime(base)
            current = output.read_text(encoding="utf-8")
            findings = runtime.Contract(base).validate_text(current, "operations/priority-dashboard.md", resolve_relations=True)
            failures = [finding for finding in findings if finding.level == "fail"]
            saved_digest = saved_source_digest(current)
            if failures or saved_digest != source_digest(base):
                print("priority-dashboard: drift")
                return 1
            print("priority-dashboard: current")
            return 0
        rendered, selection, control = build(base, args.reason, args.timezone, args.as_of)
        output.write_text(rendered, encoding="utf-8")
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"priority-dashboard: fail: {exc}", file=sys.stderr)
        return 1
    mode = "manual-active" if control.effective(datetime.now().date()) else "generated"
    print(
        "priority-dashboard: updated "
        f"focus={len(selection.today)} next7={len(selection.week)} life30={len(selection.life_horizon)} "
        f"waiting={len(selection.waiting_actions)} triggers={len(selection.due_triggers)} "
        f"admin={len(selection.admin_actions)} stale={len(selection.urgent_not_focus)} mode={mode}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
