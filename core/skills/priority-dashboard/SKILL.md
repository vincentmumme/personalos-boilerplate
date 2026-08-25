---
name: priority-dashboard
description: "Use this to rebuild, inspect, or temporarily steer {{user_name}}'s current PersonalOS priority dashboard from canonical Actions, Attention Triggers, and owner context. Do NOT use it to create, complete, or independently manage tasks; use task-manager for Action and Trigger lifecycle changes."
metadata:
  pos_schema_version: pos-v1
  pos_id: 01a0251c-9e64-7f0d-81a6-bf5efd9bc4d7
  pos_type: skill
  pos_title: "Skill: priority-dashboard"
  pos_created: "2026-08-21"
  pos_updated: "2026-08-22"
  pos_lifecycle: active
  pos_skill_version: 1.2.0
  pos_system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/operations/action-und-attention-modell]]", "[[system/frameworks/operations/priority-dashboard]]", "[[system/rules/core/timezone-and-local-day-boundary]]"]
  pos_reads_profile_keys: ["action", "attention-trigger", "project", "priority-control", "view-record"]
  pos_writes_profile_keys: ["priority-control", "view-record"]
  pos_template_refs: ["[[system/templates/operations/priority-control]]", "[[system/templates/topology/view-record]]"]
  pos_invokes_skill_refs: ["[[skills/task-manager/SKILL]]", "[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: priority-dashboard

## Contract

This skill produces exactly one current read model at priority dashboard. It reads canonical Actions, due Attention Triggers, relevant linked owner state, and the optional temporary priority control. It never owns task text, deadlines, evidence, completion, lifecycle, project truth, or recurring commitments.

The dashboard contains no checkboxes and no independent completion controls. Every surfaced item links to its canonical Action or Trigger and states why it is prioritized. The bounded view contains exactly one current focus, at most three next-seven-day outcomes, and enough 30-day life gates to keep the combined main-focus set at no more than five Actions. Waiting/cashflow risk and stale review remain separate lanes. Routine receipt/Admin work is invisible outside the final five calendar days and then appears only as a month-end batch; payment and material risk exceptions stay in the risk lanes.

Ranking follows [[system/frameworks/operations/priority-dashboard]]: effective {{user_name}} control first, then real `due` deadlines inside a rolling seven-day horizon, explicit `critical`/`high` priority and actual `in-progress` work, linked owner impact, soft `target` tie-breaking, and finally opportunities. A `target` never creates focus by itself. Free-text cadence words never affect rank. An expired control is ignored automatically and remains visibly identified as expired.

## Rebuild

Run from the PersonalOS root:

```bash
python3 skills/priority-dashboard/scripts/rebuild.py --reason manual
```

Use the explicit reason matching the event:

```bash
python3 skills/priority-dashboard/scripts/rebuild.py --reason manual-priority-change
python3 skills/priority-dashboard/scripts/rebuild.py --reason operational-state-change
```

The scheduled VPS run uses `--reason scheduled --timezone Europe/Berlin`. The timezone argument is explicit scheduler context, not a duplicate hidden default.

## Steering

When {{user_name}} changes focus, ordering, or exclusions:

1. Update only priority control using its registered profile and template.
2. Use canonical Action links; do not copy titles, Next Actions, Done Boundaries, or lifecycle state into the control record.
3. Set `priority_control_review_on`; an active control also requires `priority_control_expires_on`.
4. Rebuild immediately with `--reason manual-priority-change`.
5. Run `pos-verify` on the control and generated dashboard.

Manual focus and ordering affect only the read model. Exclusion hides an item from this dashboard temporarily; it does not cancel, defer, complete, or edit the Action.

## Operational Refresh

After a material Action, Trigger, or linked Project change, the supported explicit path is a rebuild with `--reason operational-state-change`. There is no realtime watcher. The daily scheduled rebuild makes the dashboard morning-ready, while explicit rebuilds cover same-day operational changes.

Before consuming the saved view, run:

```bash
python3 skills/priority-dashboard/scripts/rebuild.py --check
```

`--check` validates the saved `view-record` and compares its stored Source-Digest with the current Action, Trigger, Control, and Project sources. A mismatch is `drift`; rebuild rather than presenting stale priorities.

## Verification

Run:

```bash
python3 skills/priority-dashboard/scripts/test_rebuild.py
python3 system/data-model/scripts/pos_v1.py validate --files operations/priority-control.md operations/priority-dashboard.md
python3 skills/pos-verify/scripts/run.py --files operations/priority-control.md operations/priority-dashboard.md
```

The script validates the rendered `view-record` before writing and rejects checkbox output, an invalid active control, conflicting manual include/exclude refs, or more than five main-focus Action links.

## Failure Behavior

- Invalid or unreadable canonical Actions fail the rebuild rather than being silently reinterpreted.
- An active control without a valid expiry fails Registry validation.
- Expired control directions are ignored, not auto-renewed.
- Unknown control Action refs are surfaced as warnings and never promoted to invented tasks.
- The previous dashboard remains in place if rendering or validation fails.

## Resources

- `scripts/rebuild.py` — deterministic ranking and Markdown rebuild.
- `scripts/test_rebuild.py` — focused behavioral tests.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
