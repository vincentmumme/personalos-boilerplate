---
schema_version: pos-v1
id: 01a001a0-f1c5-78e9-9f85-7ddee5f8b266
type: template
title: "Template: Finance Client Cost"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-client-cost
---

# Template: Finance Client Cost

## Template Contract

Kanonischer Weiterbelastungszustand einer realen Kundenkostenposition; die zugrunde liegende Ausgabe bleibt eigener Owner.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
cost_period: "<cost_period>"
recharge_state: <recharge_state>
client_ref: "[[companies/example-client]]"
---

# <title>

## Current Truth

<current recharge truth>

## Cost

<cost and value>

## Recharge State

<pending, invoiced, paid or waived>

## Client and Project

<typed owner relations>

## Source Expense

<underlying expense pointer>

## Invoice Allocation

<outgoing invoice relation>

## Evidence

<source map>

## Timeline

- **<date>** | Client cost created or materially changed.
```

## Usage

Ein Record pro fachlicher Kostenposition unter `finance/client-costs/`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
