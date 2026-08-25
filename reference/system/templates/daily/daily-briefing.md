---
schema_version: pos-v1
id: 01a00149-b5ad-7b82-9318-e717c39184cb
type: template
title: "Template: Daily Briefing"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/daily/modularer-daily-kontext]]", "[[system/contracts/daily/briefing-ownership-and-delivery]]", "[[system/rules/core/timezone-and-local-day-boundary]]"]
target_profile_key: daily-briefing
---

# Template: Daily Briefing

## Template Contract

Abgeleitete, zeitgebundene Entscheidungsvorlage für einen lokalen PersonalOS-Tag. Sie priorisiert bereits vorhandene Wahrheit und Live-Kontext, besitzt aber weder fachliche Current Truth noch Automation-Run-Wahrheit.

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
briefing_kind: <briefing_kind>
producer_skill_ref: "<producer_skill_ref>"
---

# <title>

## Briefing

<exact user-facing briefing>

## Source Notes

<compact source coverage, freshness and unavailable-source notes>

## Verification

<profile, content and delivery-payload checks>

## Corrections

None.
```

## Usage

Der Pfad ist `daily/<year>/<date>/briefing/<uuid>.md`. Der Day Record muss bereits existieren. Mehrere Briefings an einem Tag sind erlaubt; die Art wird über `briefing_kind` unterschieden. Delivery bleibt ein externer Side Effect und erzeugt keine zweite POS-Kopie.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
