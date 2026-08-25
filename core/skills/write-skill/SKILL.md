---
name: write-skill
description: "Use this when the user wants to create a new shared PersonalOS skill under skills/ or revise a specified PersonalOS skill and the scope is already clear. Do NOT use for raw workflow capture or deciding whether work should become a skill; use skillify first. Do NOT use for repo-local or agent-local skills unless {{user_name}} explicitly wants promotion into PersonalOS."
metadata:
  pos_schema_version: pos-v1
  pos_id: 019fecfe-ab8a-7b1c-821f-ae844da9a988
  pos_type: skill
  pos_title: "Skill: write-skill"
  pos_created: "2026-06-21"
  pos_updated: "2026-08-11"
  pos_lifecycle: active
  pos_skill_version: 2.0.1
  pos_system_refs: ["[[system/contracts/core/system-artifact-ownership-and-capability-boundary]]", "[[system/contracts/core/capability-interface]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/runbooks/core/personalos-mutation]]", "[[system/runbooks/core/test-before-bulk]]"]
  pos_reads_profile_keys: ["skill", "template", "contract", "runbook", "check"]
  pos_writes_profile_keys: ["skill"]
  pos_template_refs: ["[[system/templates/skill]]"]
  pos_invokes_skill_refs: ["[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/system/capability-control-plane-integrity]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: write-skill

## Purpose

Create or revise one shared PersonalOS skill without inventing a second skill format, duplicating system rules inside the skill, or breaking runtime discovery. `SKILL.md` remains the single canonical skill record; `scripts/`, `references/` and `assets/` are optional local execution resources rather than companion truth records.

## Contract

This skill guarantees:

- A MECE check happens before a new skill folder is created. Extend an existing capability when it already owns the intent.
- The host runtime's authoritative skill-authoring guidance is followed for discovery, instruction quality and resource design.
- Every shared PersonalOS skill uses the runtime envelope from [[system/templates/skill]]: top-level `name` and `description`, plus the closed `pos_*` record namespace inside `metadata`.
- `pos_created` and `pos_updated` are emitted as quoted ISO-date strings so YAML loaders cannot turn them into non-JSON-serializable date objects during Runtime-Agent skill loading.
- `name` matches the lower-kebab skill folder and is not duplicated as `capability_key`.
- POS integration is declared only when present. No empty `pos_system_refs`, I/O, template, invocation or check lists are written.
- `pos_writes_profile_keys` describes POS-record writes only and always has `pos_check_refs`. External side effects are explained in the body and are not collapsed into a generic `mutating` field.
- Persisted POS-record shapes and general POS semantics come from `/system`; skill-local resources contain only execution-specific scripts, references, prompts, examples, fixtures or assets.
- New routable skills are connected to `skills/RESOLVER.md`, `skills/index.md` and representative `routing-eval.jsonl` cases.
- Every write is validated against the runtime contract, the `pos-v1` Registry, resolver health and the explicit POS postflight.

## Workflow

1. **Confirm scope and ownership.**
   Read the request, `skills/RESOLVER.md`, `skills/index.md` and the closest existing skills. If the workflow is still only a candidate, route to `skillify`. If it belongs to one repository or one agent, keep it at that narrower owner unless {{user_name}} explicitly requests a shared POS skill.

2. **Read the governing contracts.**
   Read the direct `pos_system_refs` above, the `skill` profile in `system/data-model/profiles/skill.yaml` and [[system/templates/skill]]. Apply the host's installed skill-authoring guidance when available. General POS semantics come only from the applicable owners under [[system/index]].

3. **Design the capability boundary.**
   Define the positive trigger, nearest non-goals, inputs, outputs, side effects, approval boundary, failure behavior and required resources. Keep `description` focused on selection: what the skill handles and when it must not be selected.

4. **Create or revise the single `SKILL.md`.**
   Use only `name`, `description`, optional `license`, optional `allowed-tools` and `metadata` on top level. Within `metadata`, write the eight required POS fields in Foundation order:

   ```yaml
   metadata:
     pos_schema_version: pos-v1
     pos_id: <uuidv7>
     pos_type: skill
     pos_title: "Skill: <name>"
     pos_created: "YYYY-MM-DD"
     pos_updated: "YYYY-MM-DD"
     pos_lifecycle: active
     pos_skill_version: 1.0.0
   ```

   Preserve `pos_id` and `pos_created` on revision. Add capability fields only for real POS interfaces. Structure the body for the job; there is no universal mandatory H2 list.

5. **Place resources by authority.**
   Put reusable code in `scripts/`, detailed execution documentation or examples in `references/`, and non-context output resources in `assets/`. Move any general rule, convention, framework, runbook, check or persisted POS-record template to its canonical `/system` owner and reference it from the skill.

6. **Update routing surfaces when needed.**
   For a new routable skill, add a precise Resolver route, a navigation entry and at least three realistic positive routing evals. Revisions change these surfaces only when the selection boundary changed. Do not make `skills/index.md` a second resolver.

7. **Validate the smallest representative slice.**
   Run the available host runtime validator for the skill directory. Then run:

   ```bash
   python3 system/data-model/scripts/pos_v1.py validate --files skills/<name>/SKILL.md
   python3 system/checks/system/scripts/check-resolvable.py
   python3 skills/pos-verify/scripts/run.py --files <explicit-changed-files>
   ```

   Run skill-local tests or scripts when present. If several skills or records will change, apply [[system/runbooks/core/test-before-bulk]] before expanding beyond the pilot.

8. **Rebuild exposure.**
   Run `system/checks/system/scripts/check-resolvable.py` when the shared skill surface changed, or report it as an explicit next step if the current environment cannot safely execute it.

## Output Format

A successful run reports:

- created or revised canonical `SKILL.md` and any justified local resources;
- whether Resolver, index and routing evals changed or were explicit no-ops;
- runtime-validator, Registry, resolver, local-test and `pos-verify` results;
- external side effects, approvals or partial writes, if any;
- relink status.

## Anti-Patterns

- Creating a second canonical skill file such as `CAPABILITY.md`.
- Restoring the Legacy flat fields `schema_version`, `type`, `role`, `status`, `version`, `triggers`, `tools` or `mutating` on top level.
- Copying rules or POS-record templates into a skill because the proper `/system` owner is missing.
- Treating every external side effect as a POS-record mutation, or omitting checks when the skill actually writes POS records.
- Requiring every skill to use the same body sections or local resource folders.
- Adding broad discovery language that overlaps another skill without an explicit negative boundary.
- Creating `LEARNINGS.md`, scratch queues, feedback queues or second task lists.
- Bulk-migrating existing skills merely because the new envelope exists.

## Resources

- `filesystem` — reads and writes the explicit skill package and routing surfaces.
- `shell` — runs runtime, Registry, resolver, local test, postflight and relink checks.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
