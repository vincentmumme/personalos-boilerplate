---
name: pos-verify
description: "Use this immediately after files are created, edited, moved, deleted, or materially rewritten inside PersonalOS. Verifies that new truth was routed to the correct owner, written in the correct file shape, and still follows POS conventions. Do NOT use for whole-vault deep audits; use system-health-check."
metadata:
  pos_schema_version: pos-v1
  pos_id: 019fecf7-f30c-7523-83fb-905273248f39
  pos_type: skill
  pos_title: "Skill: pos-verify"
  pos_created: "2026-06-21"
  pos_updated: "2026-08-14"
  pos_lifecycle: active
  pos_skill_version: 1.9.3
  pos_system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/contracts/core/capability-interface]]", "[[system/frameworks/core/verification-ownership]]", "[[system/runbooks/core/test-before-bulk]]"]
  pos_reads_profile_keys: ["project", "working-note", "redirect", "truth-system", "principle", "rule", "contract", "convention", "framework", "template", "runbook", "check", "skill"]
  pos_check_refs: ["[[system/checks/core/personalos-mutation-postflight]]", "[[system/checks/core/markdown-record-integrity]]", "[[system/checks/pos-v1-contract]]", "[[system/checks/system/capability-control-plane-integrity]]", "[[system/checks/migration/pos-gbrain-v1-compatibility]]"]
---

# Skill: pos-verify

> **System dependencies:** [[system/contracts/core/personalos-mutation-contract]], [[system/checks/core/personalos-mutation-postflight]], [[system/contracts/core/capability-interface]] und [[system/frameworks/core/verification-ownership]].
> **Bulk guard:** [[system/runbooks/core/test-before-bulk]].

## Contract

This skill guarantees:

- Verification is write-scoped: it checks files changed in the current run plus the propagation map and any adjacent no-op targets needed to validate routing.
- Verification is both semantic and deterministic. The script is a baseline, not the whole review.
- Every static Finding Code emitted by the runner is mapped to exactly one declarative Check owner; the mapping test blocks silent unmapped additions or removals.
- The new truth, source/evidence, target owner, section placement, provenance, Current Truth synthesis, State/Open Threads, Timeline behavior, and no-op decisions are checked against the relevant conventions.
- Explicit file lists from the owning writer are preferred over Git discovery.
- The runner resolves the owning PersonalOS vault from its own installed script path before consulting the caller's working directory, so absolute invocations outside the vault do not turn valid wikilinks into false broken-link warnings.
- Git-diff fallback is available when no explicit file list exists, but large dirty trees are flagged as unreliable.
- Findings return `pass`, `warn`, or `fail` with file-level remediation.
- `pos-gbrain-v1` files are checked against their profile: person, company, deal, project, program, source, or automation-output.
- Files declaring `schema_version: pos-v1` are resolved through `system/data-model/registry.yaml` and checked for the six-field Foundation, UUIDv7 identity, registered Primary Profile, field ownership, types/enums, path, Page Shape sections, conditional state rules, typed relations, Title/H1 equality and duplicate IDs.
- Changes to the canonical data-model Registry fail when generated Field-/Profile-Indizes or per-profile JSON Schemas drift; generated artifacts are rebuilt from the Registry and never edited independently.
- Explicit interaction scan reports under `_system/runs/` with `type: source` and `role: run-report` keep the source profile even though they live beside automation artifacts; dated producer outputs under `automations/*/outputs/` use the automation-output profile.
- Person/company quality checks warn when Current Truth exceeds 500 words; project/deal/program checks warn above 400 words. All five canonical entity/work profiles warn when State exceeds 12 bullets or Open Threads exceeds 10 bullets; project pages also warn on checkbox-based shadow task lists. These are rewrite/routing warnings, not permission to delete material truth.
- Day Records, Activity Contributions and Journal Entries are checked exclusively through their registered `pos-v1` profiles. `pos-verify` does not duplicate Daily fields or templates.
- Deep vault-wide drift remains owned by `system-health-check`.

## Phases

1. **Collect the changed files.**
   Prefer an explicit changed-file list and propagation map from the calling skill or [[system/runbooks/core/personalos-mutation]]. The map should name source/evidence, new truth, selected target files/sections, plausible no-op targets, and verification focus. If no map exists, reconstruct the likely source and targets from the current conversation and changed files; warn when reconstruction is uncertain. If no explicit file list exists, use Git discovery and name the dirty-tree risk.

2. **Run deterministic baseline verification.**
   Use:

   ```bash
   python3 skills/pos-verify/scripts/run.py --files <path> [<path> ...]
   ```

   The same command may use an absolute script path from outside the vault; root and link resolution remain anchored to the verifier's owning PersonalOS checkout.

   Fallback:

   ```bash
   python3 skills/pos-verify/scripts/run.py --changed-from git
   ```

   The runner composes explicit owner boundaries: generic Markdown/link integrity, the `pos-v1` Registry Contract, Capability Control Plane, write-scoped Postflight and befristete `pos-gbrain-v1` Compatibility. The deterministic baseline includes profile checks plus owner-health guards: person/company Current Truth >500 words, project/deal/program Current Truth >400 words, State >12 bullets and Open Threads >10 bullets produce focused warnings; checkbox-based shadow task lists in project pages also warn. Die drei modularen Daily-Profile werden wie alle anderen `pos-v1`-Records durch die Registry geprüft.

   For `pos-v1`, the runner delegates contract semantics to `system/data-model/scripts/pos_v1.py`. Do not duplicate its profile fields or enums inside this skill. A Registry/runtime load error is a blocking failure.

3. **Add focused ad-hoc verification when canonical coverage is missing.**
   If a POS write changed a Markdown automation output, report, or other artifact where no canonical test/lint/build command is detected by the runtime, create a temporary focused verifier instead of relying on prose claims. Use an OS-safe tempfile path with a `runtime-agent-verify-` filename prefix (for example via Python `tempfile.NamedTemporaryFile(prefix="runtime-agent-verify-", suffix=".py", dir=tempfile.gettempdir(), delete=False)`), run it against the changed file, and clean it up when possible. The verifier should check the concrete contract of the changed artifact: required frontmatter, required headings/sections, expected item counts, required fields, changed-file metadata, and lightweight Markdown link fetches/local-link existence when links were part of the work. Summarize this as **ad-hoc targeted verification**, not as full suite green.

   If the runtime explicitly reports `workspace ... unverified` and names an exact temp directory, rerun the ad-hoc verifier as a real standalone temp file in that exact directory, not only as tool-internal subprocess logic or a verifier hidden inside another Python script. Print or otherwise surface the created `runtime-agent-verify-*` path, execute `/opt/homebrew/bin/python3 <that-file>` (or the local Python for the environment), remove the file, and report `temp_script_removed=True` when cleanup succeeded. For code edits, the verifier must exercise the changed behavior, not just inspect text; for example, import the helper in a scratch fixture and assert the new output shape/EOF/marker behavior.

   If the inline `NamedTemporaryFile` creation command itself is rejected by the Runtime-Agent lifecycle guard before Python starts, do not treat the artifact as unverified and do not disable the guard. Retrieve the exact OS temp directory with a short bare-interpreter command, create the `runtime-agent-verify-*.py` file there through the filesystem/write tool, then execute that standalone file with the bare interpreter token and remove it. Record the initial guard rejection as a runtime tooling retry, not as a target-file defect.

   Prefer Python standard-library-only standalone verifiers on the Service-Host. `/opt/homebrew/bin/python3` may not include PyYAML, so do not `import yaml` unless dependency presence was verified first; flat Markdown frontmatter checks should use a small stdlib parser or direct line assertions. If an optional import fails, repair and rerun the same standalone verifier before reporting targeted verification as passed.

   For narrow edits inside large legacy files, keep ad-hoc checks scoped to the changed behavior and newly written blocks. New Action/Attention records are not legacy exceptions: validate their complete `pos-v1` contract and links. Broad checks on unrelated legacy files remain out of scope unless the run explicitly migrates them.

4. **Run semantic propagation verification.**
   For every changed or deliberately no-oped target, read the relevant convention/profile and check:
   - the truth is in the canonical owner, not only in a log, interaction, source, automation output or todo;
   - nearby person/company/deal/project/program/domain/action/evidence owners that should change are changed, and nearby owners that should not change have a clear no-op reason;
   - Current Truth remains a short present-tense synthesis, not an appended timeline, backlog or transcript summary;
   - `State`, `Open Threads`, `Decisions`, `Relationship`, `Communication Profile`, finance/status sections or other profile sections were updated when the new truth changed them;
   - Timeline entries exist only for real events/file changes, are dated, and do not contain future placeholders;
   - source/provenance is strong enough for new claims, with privacy/secrets redacted;
   - frontmatter `updated`, status fields, tags and profile fields still serve routing/query needs and do not become a second body;
   - no active task truth exists outside `operations/actions/` and `operations/attention-triggers/`, and project files do not copy repo implementation truth.

4. **Interpret the combined result.**
   Treat `fail` as blocking unless the user explicitly accepts the risk. Treat `warn` as migration debt or likely drift to fix or report.

5. **Fix or report.**
   Fix issues that are safe and in scope. Report blocked findings with affected file, reason, and recommended next action.

## Output Format

A successful run produces:

- `pass`, `warn`, or `fail`.
- The checked file count.
- A semantic routing verdict: correct owner, missing owner, unnecessary owner, or uncertain owner.
- Findings grouped by file with severity, code, message, and remediation.
- Any no-op target decisions that were verified or remain questionable.
- No persistent report by default. JSON output is available via `--json`.

## Anti-Patterns

- Reintroducing caller-CWD-only root detection; absolute verifier invocations from cron or session contexts must remain anchored to the owning PersonalOS vault.
- Running a whole-vault audit after every write.
- Treating a deterministic script pass as sufficient when new truth or canonical state changed.
- Trusting broad Git discovery in a heavily dirty vault without naming the ambiguity.
- Treating warnings as invisible.
- Verifying only syntax while missing that the truth belongs in another canonical file.
- Approving Current Truth bloat, duplicate live truth, timeline-only updates, or task drift because headings/frontmatter happen to pass.
- Using `pos-verify` instead of the owning domain skill for actual work.

## Tools Used

- `filesystem` — read changed files and nearby indexes needed for link resolution.
- `shell` — run `skills/pos-verify/scripts/run.py` and supporting checks.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
