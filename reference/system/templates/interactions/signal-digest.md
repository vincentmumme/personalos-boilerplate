---
schema_version: pos-v1
id: 01a0020f-303d-7fe5-b8a6-0252d626a97c
type: template
title: "Template: Signal Digest"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/rules/automations/material-run-receipt-retention]]"]
target_profile_key: signal-digest
---

# Template: Signal Digest

## Template Contract

Quellengebundene, nicht-kanonische Verdichtung äußerer News-, Web- oder Creator-Signale. Der Digest besitzt weder fachliche Current Truth noch eine versteckte Content-Idea; `/automations` hält ausschließlich den Verarbeitungslauf.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: signal-digest
title: "<title>"
created: <date>
updated: <date>
digest_date: <date>
digest_kind: <digest_kind>
digest_outcome: <digest_outcome>
coverage_started_at: <coverage_started_at>
coverage_ended_at: <coverage_ended_at>
producer_skill_ref: "[[skills/<skill>/SKILL]]"
---

# <title>

## Digest Summary

<bounded synthesis>

## Coverage

<source window, retrieval coverage and dedupe>

## Signals

<ranked source-bounded signals>

## Source Map

<canonical URLs, timestamps and provenance>

## Propagation

<no-op, candidate handoff or explicit owner updates>

## Gaps and Corrections

<fetch gaps, uncertainty and later corrections>
```

## Usage

Ein Producer schreibt höchstens einen Digest pro Kalendertag unter `interactions/signals/<producer>/<year>/<date>.md`. Wiederholte Runs aktualisieren denselben Tagesrecord quellengebunden; dauerhafte fachliche Wahrheit wird zuerst zum zuständigen Owner propagiert. ContentOS übernimmt nur eine von {{user_name}} oder einem klaren Workflow bewusst ausgewählte Richtung.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
