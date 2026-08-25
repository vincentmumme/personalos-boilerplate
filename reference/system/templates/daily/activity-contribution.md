---
schema_version: pos-v1
id: 019ff260-fbc9-77e6-938c-e266b670806c
type: template
title: "Template: Activity Contribution"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/daily/modularer-daily-kontext]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
target_profile_key: activity-contribution
---

# Template: Activity Contribution

## Template Contract

Instanzvorlage für einen atomaren, deduplizierbaren Beitrag darüber, was ein Mensch, Agent, Prozess oder externes System tatsächlich gearbeitet oder bewirkt hat.

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
activity_outcome: <activity_outcome>
affected_owner_refs: <affected_owner_refs>
---

# <title>

## Activity

<what was worked on, checked or changed>

## Outcome

<material result; omit technical step-by-step noise>

## Affected Owners

- <canonical owner links and propagation outcome>

## Evidence

- <source, receipt, decision or changed-record links>

## Corrections

None.
```

## Usage

Der Pfad ist `daily/<year>/YYYY-MM-DD/activity/<uuid>.md`. Reine technische Zwischenschritte und wiederholte No-ops erzeugen keinen einzelnen Record; sie werden ausgelassen oder zu einer materiellen Contribution aggregiert. Owner-Propagation geschieht vor dem Daily Write.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
