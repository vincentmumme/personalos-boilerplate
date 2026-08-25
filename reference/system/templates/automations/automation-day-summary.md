---
schema_version: pos-v1
id: 019ff59c-3182-7aa5-943b-fded3e0a1cb6
type: template
title: "Template: Automation Day Summary"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/rules/automations/material-run-receipt-retention]]"]
target_profile_key: automation-day-summary
---

# Template: Automation Day Summary

## Template Contract

Genau ein kompakter Tagescontainer pro Automation und Kalendertag. Er beweist vollständige Coverage einschließlich unterdrückter Routine-No-ops und verlinkt materielle Einzelbelege.

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
processed_until: <processed_until>
producer_skill_ref: "<producer_skill_ref>"
retention_class: daily-aggregate
day_summary_outcome: <day_summary_outcome>
---

# <title>

## Run Summary

<total, material, no-op, failed and pending counts>

## Coverage

<source coverage and freshness>

## Material Receipts

<links or none>

## No-op Accounting

<count and grouped reasons without individual files>

## Failures and Pending

<open states or none>

## Propagation

<affected owners and deliberate no-ops>

## Corrections

None.
```

## Usage

Der Zielpfad ist `automations/<automation-slug>/daily/<year>/YYYY-MM-DD.md`. Der Record enthält keine kopierte Source Evidence oder Domain Truth.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
