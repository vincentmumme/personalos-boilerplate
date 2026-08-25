---
schema_version: pos-v1
id: 01a001a0-f1f0-7359-bec3-41ef670701e5
type: template
title: "Template: Finance Time Entry"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-time-entry
---

# Template: Finance Time Entry

## Template Contract

Abrechenbare oder bewusst nicht abrechenbare Leistungszeit mit eigener Billing State Machine.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
service_date: <service_date>
billing_state: <billing_state>
client_ref: "[[companies/example-client]]"
hours: "<hours>"
---

# <title>

## Current Truth

<current billing truth>

## Service

<delivered service>

## Time and Value

<hours, rate and value>

## Billing State

<unbilled, invoiced, paid or excluded>

## Client and Project

<typed relations>

## Invoice Allocation

<invoice pointer when allocated>

## Evidence

<delivery evidence>

## Timeline

- **<date>** | Time entry created or materially changed.
```

## Usage

Ein Record pro fachlich zusammengehöriger Leistungsposition unter `finance/client-hours/`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
