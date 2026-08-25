---
schema_version: pos-v1
id: 019ff260-fba5-777a-aa08-22d13491a716
type: template
title: "Template: Day Record"
created: 2026-08-11
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/daily/modularer-daily-kontext]]", "[[system/conventions/core/record-naming-and-temporal-paths]]"]
target_profile_key: day-record
---

# Template: Day Record

## Template Contract

Instanzvorlage für die kompakte, aus atomaren Beiträgen abgeleitete Tagesübersicht. Sie ist weder zweite Domain Truth noch Automation Log.

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
---

# <title>

## Day Summary

<compact summary of the day>

## Key Outcomes

- <meaningful outcome>

## Activity Contributions

- <activity links or "None.">

## Journal

- <journal links or "None.">

## Affected Owners

- <links to canonical owners changed that day>

## Sources

- <contribution, evidence and source links>

## Corrections

None.
```

## Usage

Der Pfad ist `daily/<year>/YYYY-MM-DD/YYYY-MM-DD.md`. Die Datei wird nur erzeugt, wenn mindestens eine relevante Activity Contribution, ein Journal Entry oder ein zugelassenes Tagesmodul wie Daily Briefing beziehungsweise Context Gap Review existiert. `activity_refs`, `journal_refs`, `briefing_refs` und `context_gap_refs` werden nur bei vorhandenen Records gesetzt. Der Assembler darf Summary und Linklisten aktualisieren; fachliche Wahrheit bleibt bei ihren Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
