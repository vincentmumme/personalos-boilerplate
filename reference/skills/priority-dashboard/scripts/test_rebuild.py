#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = Path(__file__).with_name("rebuild.py")
SPEC = importlib.util.spec_from_file_location("priority_dashboard_rebuild", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def action(
    ref: str,
    *,
    due: str | None = None,
    target: str | None = None,
    follow_up_at: str | None = None,
    lifecycle: str = "ready",
    priority: str | None = "normal",
    owner_priority: str = "normal",
    owner_workflow: str | None = None,
    opportunity: bool = False,
    with_owner: bool = True,
    title: str | None = None,
    current_truth: str = "Open commitment.",
    affected_refs: list[str] | None = None,
):
    owner = MODULE.OwnerContext(
        ref="projects/example/example",
        title="Example",
        lifecycle="active",
        priority=owner_priority,
        commercial_state="open" if opportunity else "won",
        project_phase="discovery" if opportunity else "delivery",
        workflow=owner_workflow,
    )
    return MODULE.Action(
        path=ROOT / f"operations/actions/{ref}.md",
        ref=f"operations/actions/{ref}",
        title=title or ref,
        lifecycle=lifecycle,
        action_priority=priority,
        due=date.fromisoformat(due) if due else None,
        target=date.fromisoformat(target) if target else None,
        not_before=None,
        follow_up_at=date.fromisoformat(follow_up_at) if follow_up_at else None,
        updated=date(2026, 8, 21),
        next_action="Do the next observable step.",
        desired_outcome="Outcome is proven.",
        current_truth=current_truth,
        affected_refs=affected_refs or [],
        owner_contexts=[owner] if with_owner else [],
    )


class PriorityDashboardRebuildTest(unittest.TestCase):
    def test_effective_manual_focus_beats_deadline(self) -> None:
        today = date(2026, 8, 21)
        manual = action("manual")
        deadline = action("deadline", due="2026-08-21")
        control = MODULE.Control(
            lifecycle="active",
            review_on=today,
            expires_on=date(2026, 8, 22),
            focus_refs=[manual.ref],
        )
        selection = MODULE.select([deadline, manual], [], control, today)
        self.assertEqual(manual.ref, selection.today[0].ref)

    def test_expired_control_is_ignored(self) -> None:
        today = date(2026, 8, 21)
        manual = action("manual")
        deadline = action("deadline", due="2026-08-21")
        control = MODULE.Control(
            lifecycle="active",
            review_on=date(2026, 8, 20),
            expires_on=date(2026, 8, 20),
            focus_refs=[manual.ref],
        )
        selection = MODULE.select([manual, deadline], [], control, today)
        self.assertEqual(deadline.ref, selection.today[0].ref)

    def test_soft_target_does_not_beat_critical_or_in_progress(self) -> None:
        today = date(2026, 8, 21)
        soft_target = action("soft-target", target="2026-08-20")
        critical = action("critical", priority="critical", with_owner=False)
        active = action("active", lifecycle="in-progress", with_owner=False)
        ranked = sorted(
            [soft_target, active, critical],
            key=lambda item: MODULE.action_rank(item, today, today.replace(day=27), MODULE.Control()),
        )
        self.assertEqual([critical.ref, active.ref, soft_target.ref], [item.ref for item in ranked])

    def test_weekly_words_are_not_a_priority_signal(self) -> None:
        today = date(2026, 8, 22)
        false_recurring = action(
            "false-recurring",
            title="Im Weekly besprochene Betriebsfrage",
            current_truth="Der Daily-Call-Betrieb bleibt offen.",
        )
        high = action("high", priority="high", with_owner=False)
        ranked = sorted(
            [false_recurring, high],
            key=lambda item: MODULE.action_rank(item, today, today.replace(day=28), MODULE.Control()),
        )
        self.assertEqual(high.ref, ranked[0].ref)

    def test_saturday_sees_a_real_deadline_on_wednesday(self) -> None:
        today = date(2026, 8, 22)
        deadline = action("z-deadline", due="2026-08-26")
        project_fallback = action("a-project", owner_priority="high")
        selection = MODULE.select([project_fallback, deadline], [], MODULE.Control(), today)
        self.assertEqual(deadline.ref, selection.today[0].ref)

    def test_critical_action_beats_normal_high_project_fallback(self) -> None:
        today = date(2026, 8, 22)
        critical = action("critical", priority="critical", with_owner=False)
        project_fallback = action("project", owner_priority="high")
        ranked = sorted(
            [project_fallback, critical],
            key=lambda item: MODULE.action_rank(item, today, today.replace(day=28), MODULE.Control()),
        )
        self.assertEqual(critical.ref, ranked[0].ref)

    def test_current_focus_is_single_and_next_seven_days_are_bounded(self) -> None:
        rendered, selection, _ = MODULE.build(ROOT, "manual", "Europe/Berlin", "2026-08-22T05:40:00+02:00")
        self.assertLessEqual(len(selection.today), 1)
        self.assertLessEqual(len(selection.week), 3)
        self.assertIn("### Aktueller Fokus", rendered)
        self.assertIn("### Nächste sieben Tage", rendered)

    def test_saved_digest_parser_rejects_stale_dashboard(self) -> None:
        current = (ROOT / "operations/priority-dashboard.md").read_text(encoding="utf-8")
        saved = MODULE.saved_source_digest(current)
        self.assertIsNotNone(saved)
        self.assertEqual(saved, MODULE.source_digest(ROOT))

    def test_client_delivery_waiting_beats_earlier_personal_waiting(self) -> None:
        today = date(2026, 8, 22)
        personal = action(
            "personal-waiting",
            lifecycle="waiting",
            priority="high",
            follow_up_at="2026-08-23",
            with_owner=False,
        )
        client = action(
            "client-waiting",
            lifecycle="waiting",
            priority="high",
            follow_up_at="2026-08-26",
            owner_workflow="delivery",
        )
        selection = MODULE.select([personal, client], [], MODULE.Control(), today)
        self.assertEqual(client.ref, selection.waiting_actions[0].ref)

    def test_routine_admin_receipts_only_surface_in_month_end_window(self) -> None:
        receipt = action(
            "receipt",
            affected_refs=["finance/recurring/example"],
            with_owner=False,
        )
        before_window = MODULE.select([receipt], [], MODULE.Control(), date(2026, 8, 22))
        in_window = MODULE.select([receipt], [], MODULE.Control(), date(2026, 8, 27))
        self.assertEqual([], before_window.admin_actions)
        self.assertEqual([receipt.ref], [item.ref for item in in_window.admin_actions])

    def test_live_render_is_bounded_and_checkbox_free(self) -> None:
        rendered, selection, _ = MODULE.build(ROOT, "manual", "Europe/Berlin", "2026-08-21T05:40:00+02:00")
        self.assertNotIn("- [ ]", rendered)
        self.assertLessEqual(len(selection.today), 1)
        self.assertLessEqual(len(selection.week), 3)
        self.assertLessEqual(len(selection.today) + len(selection.week) + len(selection.life_horizon), 5)
        for heading in (
            "### Aktueller Fokus",
            "### Nächste sieben Tage",
            "### 30-Tage-Lebens- und Reisegates",
            "### Kunden-, Cashflow- und Waiting-Risiken",
            "### Admin-Batch",
            "### Stale Review",
        ):
            self.assertIn(heading, rendered)


if __name__ == "__main__":
    unittest.main()
