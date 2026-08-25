---
name: task-manager
description: "Use this when {{user_name}} or an agent wants to add, review, prioritize, complete, defer, park, or inspect todos, open loops, confirmed actions, waiting states, or attention triggers. Maintains atomic records under operations/actions/ and operations/attention-triggers/ as the only local action truth. Do NOT use for deep thought synthesis, content writing, call analysis, Google Tasks reconciliation, or Lexware booking itself."
metadata:
  pos_schema_version: pos-v1
  pos_id: 019ffca2-37d3-73b6-a234-6836aa0e3af2
  pos_type: skill
  pos_title: "Skill: task-manager"
  pos_created: "2026-05-10"
  pos_updated: "2026-08-22"
  pos_lifecycle: active
  pos_skill_version: 2.3.0
  pos_system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/operations/action-und-attention-modell]]", "[[system/frameworks/operations/priority-dashboard]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
  pos_reads_profile_keys: ["action", "attention-trigger", "action-candidate", "idea", "capture", "project"]
  pos_writes_profile_keys: ["action", "attention-trigger", "action-candidate"]
  pos_template_refs: ["[[system/templates/action]]", "[[system/templates/attention-trigger]]", "[[system/templates/action-candidate]]"]
  pos_invokes_skill_refs: ["[[skills/priority-dashboard/SKILL]]", "[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: task-manager

## Contract

This skill guarantees:

- Each confirmed open commitment is one canonical `action` record under `operations/actions/<uuid>.md`.
- Each future reassessment without a current commitment is one canonical `attention-trigger` under `operations/attention-triggers/<uuid>.md`.
- `operations/todo.md`, indexes, briefings, Daily records, project files and automation reports are never active task stores. They may only point to or derive views from the atomic records.
- The exact schemas, sections, lifecycles and field rules come from `system/data-model/profiles/action.yaml`, `system/data-model/profiles/attention-trigger.yaml`, `system/templates/action.md` and `system/templates/attention-trigger.md`.
- A source/import run reconciles matching existing records before creating anything. The system is not append-only.
- Only a real, confirmed, personally relevant open commitment becomes an Action. Inferred work, possible improvements, raw thoughts and ideas do not enter the active action set.
- A meeting discussion, opportunity, possible pilot, suggested preparation path, or hoped-for follow-up is not a confirmed commitment. Do not set `ready`, `action_priority`, `due`, or `target` unless the source or {{user_name}} explicitly commits to the work and, for dates, to that exact timing. If no date was agreed, omit timing fields instead of manufacturing urgency.
- A later date is not automatically a task. Use an Attention Trigger when the only present need is to reassess the situation later.
- A routine incoming receipt or subscription invoice is Finance collection truth, not an immediate Action. Preserve it in the proper Finance owner and add it to the month-end booking corpus. If an Operations record is needed for the month, maintain one `deferred` booking-batch Action whose `not_before` is the first of the final five calendar days; do not create or surface one Ready Action per receipt. Real payment deadlines, dunning, suspension, cashflow, legal, disputed-performance, tax, or payment-decision risks remain separate Actions.
- `waiting` is an Action lifecycle because the commitment already exists; it requires `waiting_on` and `follow_up_at`.
- Project and domain files own durable outcome truth. Action records own the current execution boundary, timing and done condition. No mirrored checkbox list is allowed.
- When source evidence changes both durable truth and an Action, update both owners in one bounded mutation.
- Before closing an Action, propagate the result to its durable owner. Then set the Action to `completed` or `cancelled`; do not erase material audit history merely to shorten a list.
- Every Action has an observable `Done Boundary`, exactly one current `Next Action`, evidence links and one execution mode: `agent-execute`, `agent-prepare` or `human-only`.
- Keep relations typed: sources and receipts belong in `evidence_refs`; affected people, companies, projects and domain owners belong in optional `affected_owner_refs`. Never use an owner record as evidence merely to satisfy the required field.
- Dates have separate meanings: `due` is a real deadline, `target` a planned finish, `not_before` hides deferred work until a date, and `follow_up_at` rechecks waiting work.
- Prioritization is a derived, time-sensitive view. Do not encode old `P0/P1/P2` buckets as permanent record truth unless the current profile explicitly admits an `action_priority` value.
- Google Tasks is not read, reconciled or mutated by PersonalOS operations.
- Every mutation follows [[system/contracts/core/personalos-mutation-contract]] and [[system/runbooks/core/personalos-mutation]] and ends with `pos-verify` on the explicit changed-file set. There is no general write-skill between this owning capability and the target records.
- After a material Action or Attention Trigger state change, invoke [[skills/priority-dashboard/SKILL]] with `--reason operational-state-change`. This is an explicit post-mutation rebuild, not a realtime watcher and not a second lifecycle write.

## Intake Decision

Apply this sequence to every possible operation:

1. Execute or propagate immediately when safe and authorized; create no leftover Action if nothing remains.
2. Search all existing Action and Trigger records for the same commitment, object, person, project and evidence.
3. Update the matching record when one exists; never duplicate it.
4. Create an Action only when commitment, outcome, done boundary and next step are confirmed.
5. Use `waiting` when the commitment exists but the next move is external.
6. Use `deferred` when the commitment exists but should not be considered before `not_before`.
7. Create an Attention Trigger when no current Action exists but a date or event should cause contextual reassessment.
8. Route ambiguous action assumptions to the bounded candidate process. Route a consciously retained general Idea by the registered `idea` profile to exactly one owner in `identity`, `business`, `knowledge`, `finance`, `health`, or the `working` module of an existing Project. Route Content Ideas only through ContentOS. A possible future Project remains a domain Idea until the Project admission threshold is crossed. Route unresolved valuable input to `inbox/captures/`, durable truth to its domain owner, and irrelevant material to no-op.

## Phases

### Create or update an Action

1. Read `operations/actions/index.md`, search `operations/actions/`, and load the relevant project/domain/source context.
2. Reconcile duplicates and decide whether durable owner truth must change in the same mutation.
3. Generate a UUIDv7 through the registered PersonalOS data-model tooling; never hand-author one.
4. Instantiate `system/templates/action.md` and include only fields admitted by the Action profile.
5. Keep `Current Truth` current, not chronological. Put history in the append-only `Timeline`.
6. Do not enumerate Actions or Triggers in navigation indexes. The section indexes contain only stable owner boundaries and routing links; agents derive every live view directly from the atomic records.

### Change lifecycle

- `ready`: one executable next move exists.
- `in-progress`: execution has actually started.
- `waiting`: external response/input/event is required; set `waiting_on` and `follow_up_at`.
- `blocked`: an internal blocker prevents progress; set `blocked_by`.
- `deferred`: the commitment remains valid but is intentionally hidden until `not_before`.
- `completed`: the Done Boundary is proven and the result has been propagated.
- `cancelled`: the commitment was explicitly withdrawn or superseded, with evidence in Timeline.

Do not infer completion from age, silence, a passed date or apparent unimportance.

### Create or resolve an Attention Trigger

1. Search existing triggers and Actions for the same subject.
2. Create a Trigger only with a concrete `review_at` and evidence.
3. At trigger time, reread the current owner context. Then create an Action, resolve as obsolete/done, ask for missing judgment, or schedule one new Trigger.
4. Never copy the old context forward as if it were still current.

## Review and Agent Views

- User-facing task lists, Morning Briefings and reviews query the atomic records and calculate urgency from current lifecycle, dates, dependencies, evidence and {{user_name}}'s context.
- Exclude completed/cancelled records and not-yet-reached deferred work from normal open-action views.
- Surface due Waiting follow-ups and due Attention Triggers as reassessment needs, not automatically as new Actions.
- Keep views concise. The source records may contain full evidence, but the agent presents only the relevant next decision or move.
- Hygiene runs merge duplicates, surface overdue or stale records, reconcile changed source reality and report ambiguous cases. They never delete uncertain context silently.

## Verification

After a mutation:

1. Validate every changed `pos-v1` Action or Trigger against the registry contract.
2. Check UUID/path identity, required sections, conditional lifecycle fields and evidence links.
3. Check that no second active task truth was written to projects, Daily records, interactions, automation outputs, indexes or `operations/todo.md`.
4. Run `pos-verify` on the explicit changed-file list and report warnings honestly.
5. Confirm that `operations/index.md`, `operations/actions/index.md` and `operations/attention-triggers/index.md` still use the registered `owner-index` profile and contain no individual record inventory.
6. Rebuild priority dashboard after material operational changes and verify that the view only references the canonical records.

## Output Format

A successful run reports:

- Actions created, updated, completed, cancelled, deferred, blocked or moved to Waiting;
- Attention Triggers created, resolved or rescheduled;
- durable owner files updated because reality changed;
- ambiguous inputs deliberately not promoted;
- validation and `pos-verify` status.

## Anti-Patterns

- Writing new checkbox tasks into `operations/todo.md` or another rollup.
- Treating every signal, reminder, calendar date or recommendation as an Action.
- Keeping competing task truth in project Open Threads, interaction rollups, Notion or Google Tasks.
- Inventing confirmation, dates, owners, completion or priority.
- Using a Trigger when a confirmed commitment already exists, or using an Action when only future reassessment exists.
- Deleting unresolved or uncertain records merely because they are old.
- Storing long strategic thought in an Action instead of linking the owning context.

## References

- [[system/frameworks/operations/action-und-attention-modell]]
- 2026 08 11 action und koordinationsmodell
- [[system/contracts/core/personalos-mutation-contract]]
- [[system/data-model/index]]
- Action-/Attention-Cutover-Beleg

## Tools Used

- `filesystem` — read and patch Action, Trigger and affected owner records.
- `shell` — query records, generate UUIDv7 values and run focused validation.
- `pos-verify` — verify every PersonalOS mutation.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
