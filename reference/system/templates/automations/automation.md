---
schema_version: pos-v1
id: 019ff59e-9302-7a13-8d7a-64cc908a4c06
type: template
title: "Template: Automation"
created: 2026-08-12
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/rules/core/timezone-and-local-day-boundary]]"]
target_profile_key: automation
---

# Template: Automation

## Template Contract

Kanonischer Registry- und Navigationseinstieg einer Automation. Der Record besitzt Automation-Objektwahrheit und verlinkt Capability, Runtime und fachliche Owner, statt sie zu kopieren.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
automation_kind: <automation_kind>
schedule_timezone: <schedule_timezone>
---

# <title>

## Current Truth

<current automation state>

## Purpose

<why the automation exists>

## Trigger and Cadence

<trigger, expected cadence and freshness boundary>

## Capability and Runtime

<links to behavior, runtime and system owners>

## Inputs and Outputs

<source and target contracts without copied truth>

## Credentials Required

<credential identities and setup requirements without secret values>

## Health and Freshness

<current observable health and pointers>

## Timeline

- **<date>** | Automation record created.
```

## Usage

Der Zielpfad ist `automations/<automation-slug>/<automation-slug>.md`. Scheduled Automations deklarieren `schedule_timezone` als IANA-Zeitzone; nicht zeitgesteuerte Automationen lassen das Feld weg. Run-Historie und Tagesaggregate sind eigene Records; ausführbares Verhalten bleibt beim Skill oder externen Capability-Owner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
