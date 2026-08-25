---
name: log
description: Use this when a PersonalOS work session, chat outcome, personal reflection, or provided source should be persisted into the modular Daily context and any already-owned canonical files. Do NOT use for single-call processing, single-source knowledge ingestion, Gmail/WhatsApp propagation, or Lexware booking.
metadata:
  pos_schema_version: pos-v1
  pos_id: 019ffca2-37f8-7a8c-9f85-54d0c16e96c4
  pos_type: skill
  pos_title: "Skill: log"
  pos_created: "2026-04-19"
  pos_updated: "2026-08-13"
  pos_lifecycle: active
  pos_skill_version: 2.0.0
  pos_system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/daily/modularer-daily-kontext]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
  pos_reads_profile_keys: ["day-record", "activity-contribution", "journal-entry", "capture", "action", "attention-trigger", "project", "person", "company", "skill", "template"]
  pos_writes_profile_keys: ["day-record", "activity-contribution", "journal-entry", "capture", "project", "person", "company", "skill", "template"]
  pos_template_refs: ["[[system/templates/daily/day-record]]", "[[system/templates/daily/activity-contribution]]", "[[system/templates/daily/journal-entry]]", "[[system/templates/capture]]"]
  pos_invokes_skill_refs: ["[[skills/task-manager/SKILL]]", "[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: log

## Contract

This skill guarantees:

- Useful residue from an agent session is persisted as an Activity Contribution, an optional Journal Entry, or both, and when safe as concise updates to affected canonical owner files.
- `/log` is a write-back command by default, not a proposal command. Draft mode is used only when {{user_name}} asks for it or when a risky mutation cannot be skipped safely.
- Der Day Record bleibt der kompakte zeitliche Querschnitt. Activity Contributions belegen materielle Arbeit oder Wirkung; Journal Entries bewahren persönliche Gedanken und Reflexion. Keiner dieser Records wird zur parallelen Projekt- oder Domainwahrheit.
- Die Record-Formate werden ausschließlich von den registrierten Profilen `day-record`, `activity-contribution` und `journal-entry` sowie den Vorlagen unter `system/templates/daily/` bestimmt. Dieser Skill besitzt keine eigene Daily-Vorlage.
- Concrete tasks, decisions, checks, waiting states, and reassessment needs are routed through `task-manager` into the atomic Action/Attention records under `operations/`.
- Durable project, person, company, deal, finance, content, skill, automation, or interaction truth is updated only in the appropriate owner file and only when the session creates a high-confidence delta.
- Process-friction or useful-pattern signals are im passenden Daily-Record belegt und zum owning Skill, `task-manager` oder `system-health-check` geroutet, wenn sie handlungsrelevant sind. Keine separate Feedback-Queue wird erzeugt.
- Knowledge candidates are marked for later knowledge skills; this skill does not mix operative PersonalOS truth into knowledge-topic pages.
- Write boundary: this skill may create `daily/YYYY/YYYY-MM-DD/activity/<uuid>.md`, `daily/YYYY/YYYY-MM-DD/journal/<uuid>.md`, assemble the matching Day Record, update atomic Action/Attention records via `task-manager`, update affected owner files, and update a skill/reference/template/script only when {{user_name}} explicitly asked for that change in the current session.
- Capture boundary: when a session contains unresolved but materially valuable input that cannot yet be routed safely, this skill may create one atomic `capture` under `inbox/captures/<uuid>.md` from the registered profile and template. It does not mirror the full chat or create a general Idea Record.
- Approval boundary: creating new durable owner records beyond the bounded Capture allowed above, changing identity/relationship/legal/tax/pricing/strategy/finance truth, deleting/moving existing owner files, resolving contradictions, or writing raw private/sensitive material requires explicit approval or is recorded as an unresolved point. The Capture exception never authorizes a new permanent domain owner.
- Every new durable claim gets provenance through die atomare Activity/Journal-Evidenz, inline source, `Source Map`, provided source path, or explicit {{user_name}} statement.
- All PersonalOS mutations follow [[system/contracts/core/personalos-mutation-contract]] and finish with `pos-verify` on the explicit changed-file list.
- New and materially revised PersonalOS prose is written in German. Existing English records are not bulk-translated; when they are materially rewritten, consolidate the affected living truth in German. Source material retains its natural language. See 2026 08 07 sprache deutsch intern.

## Phases

1. **Determine source and write mode.**
   Source modes:
   - `implicit-chat`: current conversation context.
   - `explicit-document`: a provided path or file.
   - `explicit-topic`: only the matching topic slice of the current session.

   Write modes:
   - `quick-log`: compact Activity Contribution oder Journal Entry, usually no canonical updates.
   - `auto-log`: default direct write for normal sessions.
   - `full-log`: broader source-of-truth review for complex sessions.
   - `draft-log`: present a draft and wait for confirmation.

   If ambiguous but current chat has enough context, choose `implicit-chat` plus `auto-log`; otherwise ask once.

2. **Load minimum system context.**
   Read `INDEX.md`, `daily/index.md`, den Day Record des Zieltags, wenn er existiert, `skills/RESOLVER.md`, this skill, and only the domain files needed by detected targets. Lade verlinkte Activity-/Journal-Records nur bei Bedarf. Do not bulk-read all rules, indexes, or unrelated history.

3. **Analyze the source.**
   Identify what was worked on, decisions made, facts changed, blockers, open questions, files created/edited/discussed, entities and projects affected, task candidates, knowledge candidates, provenance gaps, and follow-up candidates for other skills. Preserve {{user_name}}'s exact wording when it carries strategic, emotional, brand, product, identity, or relationship nuance.

4. **Classify follow-ups and confidence.**
   Classify each item as activity evidence, personal journal content, operations candidate, local context point, capture, local entity point, knowledge candidate, skill/system feedback, or no-op. High-confidence low-risk deltas may be written directly to their owner. Unresolved but materially valuable input becomes one bounded Capture instead of living only as a Daily open point. Low-confidence or conflicting evidence must not mutate canonical truth without confirmation.

5. **Load affected files before editing.**
   For every likely update target, read the existing file fully, compare against current truth and timeline, and avoid creating new canonical files unless the session clearly establishes the target. Technical repo truth stays in the repo; PersonalOS project files hold business, strategic, operational, and decision context.

6. **Apply auto-write policy.**
   Safe writes include creating one material Activity Contribution, creating a Journal Entry when {{user_name}} provides genuine personal reflection, assembling their Day Record, marking clearly completed Actions done, adding/updating Waiting or Attention state through `task-manager`, creating one justified Capture for unresolved valuable input, updating already-affected owner files with concise deltas, adding timeline rows only in files changed in this run, and updating a skill/reference when {{user_name}} explicitly requested it. Reine technische Schritte und wiederholte No-ops erzeugen keinen Daily-Record. Risky writes are skipped, drafted, or asked about without blocking the safe log.

7. **Determine the correct Daily date.**
   Separate `occurred_at` from `recorded_at`. Use supplied source time, last relevant user message time, document timestamp, or actual event time for `occurred_at`. Use current write time for `recorded_at`. Der Container wird von `occurred_at` bestimmt, nicht von der aktuellen Uhr. Only use current clock as occurrence time when no reliable source time exists.

8. **Write in the right order.**
   Apply confident canonical updates and task changes first, then append timeline rows to files changed in this run. Erzeuge danach die atomare Activity Contribution beziehungsweise den Journal Entry mit deren finalen Owner-/Evidenzlinks und aktualisiere zuletzt den Day Record. For `draft-log`, do none of this until approval arrives.

9. **Follow canonical update rules.**
   Rewrite relevant current-truth passages instead of appending duplicates. Add source coverage for every new or changed factual claim. Keep existing template structure. Set `updated:` where present. Use source label `log` in timeline rows and link back to the atomaren Activity Contribution or Journal Entry only when the target file actually changed.

10. **Use the registered Daily profiles.**
    Activity Contributions follow `system/templates/daily/activity-contribution.md`; Journal Entries follow `system/templates/daily/journal-entry.md`; the compact assembler output follows `system/templates/daily/day-record.md`. UUIDv7 is the filename of each atomic contribution. `day_date`, path and `occurred_at` must agree; RFC-3339 timestamps include seconds and offset. Day Records are created only when at least one Activity or Journal record exists. Existing atomare Records werden nicht still umgeschrieben; Korrekturen folgen dem jeweiligen `Corrections`-Abschnitt.

11. **Verify and report.**
    Re-read touched files or run focused checks to confirm the intended changes landed, including target date, UUID/path, occurrence/recorded times, Day-Record-Link, backlinks, task state, and updated fields. Run `pos-verify` on every changed POS file. Report Daily records, created files, updated files, system/skill changes, follow-up candidates, skipped risky items, and remaining warnings.

12. **Handle skill improvement feedback.**
    If {{user_name}} says a skill should behave differently, codify the durable correction directly into the affected `SKILL.md`, reference, template, or script using that owning skill and the POS write loop. Do not make the log entry itself a mandatory runtime dependency.

## Output Format

A successful `quick-log` produces:

- one compact Activity Contribution or Journal Entry with occurred/recorded timestamps
- 1-4 key outcomes
- files affected or explicit `none`
- open point or explicit `none`
- context-source line
- verification result

A successful `auto-log` or `full-log` produces:

- Activity/Journal record created under the correct source date
- atomare Records und Day Record follow the registered profiles and Systemtemplates
- optional canonical owner-file updates with provenance
- optional Action/Attention updates through `task-manager`
- timeline rows only in files changed in the same run
- verification of dates, backlinks, changed files, and todo state
- a final report naming written, skipped, and deferred items

A `draft-log` produces a pre-write draft with record type, title, source mode, occurrence/recorded times, Daily target, files to update/create, task updates, system/skill changes requiring review, follow-up candidates, uncertain items, and a confirmation request. No files are changed until {{user_name}} approves.

Timeline rows use this logical shape: date, source `log`, one-line change, and backlink to the atomaren Daily-Beleg.

## Anti-Patterns

- Using `log` for a call transcript, Gmail/WhatsApp propagation, single knowledge source, receipt, invoice, or Lexware booking.
- Treating the session as automatic truth instead of distilled evidence.
- Logging under today's file when the source session happened on another date.
- Letting `occurred_at` equal `recorded_at` just because the delayed write happened now.
- Creating or appending flat `daily-log-YYYY-MM-DD.md` records or embedding a second Daily template in this skill.
- Creating a second task list, project status file, feedback queue, or profile.
- Creating weak people/company/deal/project files from vague session mentions.
- Mutating risky truth silently while trying to avoid a question.
- Duplicating context already written correctly by the active work session or creating a Record for a technical No-op.
- Adding timeline-only rows just to reference a Daily record.
- Writing raw private transcripts, secrets, credentials, or sensitive customer data.
- Broad system or skill rewrites unless {{user_name}} explicitly requested them.
- Skipping the owning mutation contract, `pos-verify`, or post-write timestamp/backlink checks.

## Tools Used

- `filesystem` — read session sources, Day Records, atomare Daily-Belege, owner files, task files, and write approved PersonalOS updates.
- `shell` — run targeted searches, timestamp/backlink checks, and verification commands.
- `task-manager` — write concrete operations to atomic Action/Attention records.
- `pos-verify` — postflight every changed PersonalOS file.
