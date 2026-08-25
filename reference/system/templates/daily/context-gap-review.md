---
schema_version: pos-v1
id: 01a0015e-8a7b-7db6-8cd8-9f706a3df81c
type: template
title: "Template: Context Gap Review"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/daily/modularer-daily-kontext]]", "[[system/contracts/daily/context-gap-review-ownership-and-propagation]]", "[[system/rules/core/timezone-and-local-day-boundary]]"]
target_profile_key: context-gap-review
---

# Template: Context Gap Review

## Template Contract

Abgeleitete, zeitgebundene Prüfung fehlenden oder unsicheren Kontexts. Sie hält Fragen, Antworten, Routing und Verifikation, aber keine zweite persönliche oder fachliche Current Truth.

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
generated_at: <generated_at>
context_gap_kind: <context_gap_kind>
producer_skill_ref: "<producer_skill_ref>"
---

# <title>

## Review

<reviewed context, previous loop and assessment boundary>

## Gap Map

<ranked gaps, uncertainty and leverage>

## Questions and Answers

<selected questions, answers or feedback according to context_gap_kind>

## Routing and Propagation

<canonical owner, proposed or completed propagation and explicit no-ops>

## Sources

<source and evidence links or a compact source-coverage statement>

## Verification

<profile, count, routing and provenance checks>

## Corrections

None.
```

## Usage

Der Pfad ist `daily/<year>/<date>/context-gaps/<uuid>.md`; der Day Record muss existieren. Ein `question-batch` enthält genau die H3-Blöcke `1` bis `5`. Jeder Block verwendet die Marker `Frage`, `Warum jetzt`, `Evidenz`, `Was verbessert sich`, `Write-back-Ziel`, `Antwortformat`, `Sensitivität` und `Score`. Antworten werden zuerst zu ihren kanonischen Ownern propagiert und im Review nur als belegter Routing-Ausgang festgehalten.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
