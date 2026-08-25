---
name: skillify
description: "Use this when {{user_name}} asks to skillify a repeated workflow, determine whether it deserves a reusable PersonalOS skill, or harden an existing workflow into a tested resolver-reachable capability. Do NOT use for one-off notes, ordinary execution, or already-specified skill authoring; use write-skill."
metadata:
  pos_schema_version: pos-v1
  pos_id: 01a0012f-51e4-7164-ac7a-1f779a1cc537
  pos_type: skill
  pos_title: "Skill: skillify"
  pos_created: "2026-06-21"
  pos_updated: "2026-08-14"
  pos_lifecycle: active
  pos_skill_version: 1.0.0
  pos_system_refs: ["[[system/contracts/core/system-artifact-ownership-and-capability-boundary]]", "[[system/contracts/core/capability-interface]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/runbooks/core/test-before-bulk]]"]
  pos_reads_profile_keys: ["skill", "skill-resolver", "owner-index"]
  pos_writes_profile_keys: ["skill"]
  pos_template_refs: ["[[system/templates/skill]]"]
  pos_invokes_skill_refs: ["[[skills/write-skill/SKILL]]", "[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/system/capability-control-plane-integrity]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: skillify

## Contract

This skill guarantees:

- Repeated real work is converted into compounding PersonalOS capability only when it has a stable trigger, repeat value, and enough logic or risk to justify a skill.
- New or improved skills are produced through the existing PersonalOS skill layer: `skills/<skill-name>/SKILL.md`, `skills/RESOLVER.md`, `skills/index.md`, `routing-eval.jsonl`, deterministic scripts when useful, and verification.
- Skillification preserves provenance, write boundaries, failure modes, tests, and resolver reachability instead of creating invisible prompt fragments or duplicate skills.
- Quality is checked before behavior is cemented: use cross-model or cross-modal review when available for substantial LLM-heavy skills, then write tests and routing evals that lock in the proven behavior.
- `write-skill` remains the canonical authoring sub-skill. This skill decides what should be skillified and orchestrates the hardening loop.
- Any POS file mutation performed while skillifying uses [[system/runbooks/core/personalos-mutation|PersonalOS mutation runbook]] with an explicit changed-file list and postflights through `pos-verify`.

## Phases

1. **Identify the skill candidate.**
   Read the current chat, supplied source, recent run artifact, workflow file, repo code, or PersonalOS context that produced the repeatable pattern. If the source is an external URL or article, use `source-extract` or a stable source pointer before writing durable claims. Capture the candidate name, actual user trigger phrases, repeated steps, edge cases, write targets, external systems, and observed failures.

2. **Reject non-skills early.**
   Do not skillify unless at least one of these is true: the workflow will be invoked at least twice, it contains more than trivial instructions, it touches canonical truth or external systems, it has a stable user phrase, it needs deterministic code, or failure would create meaningful drift. If it is a one-off, answer with the narrower artifact: note, script, todo, reference, or direct execution.

3. **Run the MECE check.**
   Read `skills/RESOLVER.md`, `skills/index.md`, and likely overlapping `skills/*/SKILL.md` files. If an existing skill owns the intent, update that skill or route through it. If the new skill is an orchestrator over existing skills, state the boundaries explicitly so it does not duplicate their contracts.

4. **Extract the reusable procedure.**
   Separate stable procedure from per-run parameters. Keep stable: trigger language, preconditions, read targets, write targets, decision gates, edge cases, failure modes, verification, and handoff behavior. Turn per-run details into parameters such as target, source, date window, account, format, question, dataset, or output path.

5. **Design the Skillify checklist.**
   For the candidate, decide which checklist items apply:
   - `SKILL.md` with required PersonalOS frontmatter and body sections.
   - Deterministic code under `skills/<skill>/scripts/` when code can do the repeatable part better than prose.
   - Quality review or cross-model/cross-modal eval for substantial LLM-heavy output.
   - Unit tests for deterministic logic.
   - Integration or E2E smoke tests for external endpoints, file mutations, or multi-step side effects.
   - LLM eval cases when correctness depends on judgment, extraction quality, ranking, synthesis, or writing quality.
   - Resolver entry with real user language.
   - `routing-eval.jsonl` with at least three real intents for routable skills.
   - Passing `python3 system/checks/system/scripts/check-resolvable.py`.
   - Provenance, write boundaries, draft/approval behavior, partial-write handling, and test-before-bulk when relevant.
   - Exposure rebuild via `system/checks/system/scripts/check-resolvable.py`.

6. **Author or update the skill.**
   Use `write-skill` for new shared PersonalOS skills. For existing skills, edit the narrowest owning `SKILL.md`, reference, script, test, or convention. Route all PersonalOS file mutations through [[system/runbooks/core/personalos-mutation|PersonalOS mutation runbook]], keep the changed-file list explicit, and do not create `LEARNINGS.md`. Do not create a parallel resolver. Do not promote repo-local or vendored framework skills into PersonalOS unless the reusable capability belongs at shared PersonalOS scope.

7. **Quality-review before tests lock behavior.**
   For substantial LLM-heavy skills, run an available cross-model review, NotebookLM advisor, or explicit multi-model critique against the hardest representative input before writing final tests. If no cross-model tool is available, do a manual structured review and record the waiver in the run report or final answer. Skip this gate for trivial outputs under 200 tokens, thin API wrappers, or purely deterministic scripts.

8. **Write tests and routing evals.**
   Add focused tests under `tests/` when the invariant spans the PersonalOS skill system, resolver, report contract, or shared runtime behavior. Keep skill-local helper tests or live checkers under `skills/<skill>/scripts/` when they are closer to the tool. Add `routing-eval.jsonl` for every new natural-language-routable skill.

9. **Audit and verify.**
   Run the local audit for the target skill:
   ```bash
   python3 skills/skillify/scripts/audit.py <skill-slug>
   ```
   Then run:
   ```bash
   python3 system/checks/system/scripts/check-resolvable.py
   python3 -m unittest discover -s tests
   system/checks/system/scripts/check-resolvable.py
   ```
   Fix errors before finishing. If a check is impossible in the current environment, state the exact skipped command and why.

10. **Report the durable change.**
    Summarize the candidate decision, files changed, tests run, remaining gaps, and whether the result is fully skillified or intentionally partial. If a future improvement is a confirmed commitment or reassessment need, route it through atomic Action/Attention records via `task-manager`; otherwise leave it with its proper context owner, not in an unowned note.

## Output Format

A successful run produces:

- A newly created or improved `skills/<skill-name>/SKILL.md`, or a clear rejection explaining why the workflow is not a skill.
- Updated `skills/RESOLVER.md`, `skills/index.md`, and `routing-eval.jsonl` for routable skills.
- Deterministic scripts and tests when the repeatable logic or risk warrants them.
- A passing `python3 skills/skillify/scripts/audit.py <skill-slug>` check for the skillified target, or an explicit list of non-applicable and still-open checklist items.
- Passing `python3 system/checks/system/scripts/check-resolvable.py`, relevant test commands, and a completed or explicitly deferred `system/checks/system/scripts/check-resolvable.py`.

## Anti-Patterns

- Skillifying one-off work just because it feels interesting.
- Creating a new skill when an existing skill should be extended.
- Writing a broad meta-skill that quietly owns another skill's domain.
- Freezing mediocre LLM behavior with tests before doing any quality review.
- Adding resolver entries with internal jargon instead of phrases {{user_name}} or an agent would actually say.
- Writing code with no `SKILL.md`, or `SKILL.md` with no path to invocation.
- Skipping routing evals for a new routable skill.
- Treating cross-model review as vanity scoring without applying fixes.
- Letting auto-generated skills mutate canonical files without provenance, write boundaries, failure modes, and verification.
- Creating `LEARNINGS.md`, scratch queues, or second todo lists instead of updating the owning skill, system rule or convention, script, reference, template, or atomic Action/Attention record.

## Tools Used

- `filesystem` — read the workflow source, existing skills, resolver, index, conventions, scripts, tests, and write the skillified artifacts.
- `shell` — run `skills/skillify/scripts/audit.py`, `system/checks/system/scripts/check-resolvable.py`, unit tests, integration checks, and `system/checks/system/scripts/check-resolvable.py`.
- `web` — read upstream public skill/source material when {{user_name}} supplies an external URL or when current primary-source verification is required.
