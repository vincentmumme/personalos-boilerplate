---
schema_version: pos-v1
id: 019ff260-fbf1-7e5b-bcf4-f1920e260db0
type: template
title: "Template: Journal Entry"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/daily/modularer-daily-kontext]]"]
target_profile_key: journal-entry
---

# Template: Journal Entry

## Template Contract

Instanzvorlage für einen optionalen persönlichen Tagebuch-, Reflexions-, Gedanken- oder Gesprächseintrag. Ein Journal Entry ist zeitgebundene Evidenz und nicht automatisch fachliche Current Truth.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
day_date: <day_date>
timezone: <timezone>
occurred_at: <occurred_at>
recorded_at: <recorded_at>
producer_kind: <producer_kind>
producer_name: "<producer_name>"
journal_kind: <journal_kind>
---

# <title>

## Journal Entry

<personal entry in {{user_name}}'s own meaning and nuance>

## Context

<optional situational context>

## Sources

- <conversation, note or source; use "{{user_name}}" when directly stated>

## Corrections

None.
```

## Usage

Der Pfad ist `daily/<year>/YYYY-MM-DD/journal/<uuid>.md`. Mehrere Einträge pro Tag sind zulässig. Relevante dauerhafte Wahrheit wird zusätzlich zum fachlichen Owner propagiert; Secrets bleiben ausgeschlossen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
