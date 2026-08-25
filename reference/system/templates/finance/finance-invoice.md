---
schema_version: pos-v1
id: 01a001a0-f218-7d7c-9410-b7bd6444eadf
type: template
title: "Template: Finance Invoice"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-invoice
---

# Template: Finance Invoice

## Template Contract

Agentisch relevante Projektion einer Ausgangsrechnung; Lexware bleibt Owner der formalen Rechnungs- und Zahlungswahrheit.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
issued_on: <issued_on>
invoice_state: <invoice_state>
invoice_number: "<invoice_number>"
client_ref: "[[companies/example-client]]"
external_authority_ref: "[[examples/external-authority]]"
amount_net: "<amount_net>"
amount_gross: "<amount_gross>"
currency: "<currency>"
---

# <title>

## Current Truth

<current invoice and payment truth>

## Invoice

<number, dates and formal context>

## Service and Amounts

<service and exact values>

## Delivery

<draft, finalization and delivery evidence>

## Payment State

<open, overdue, paid or voided>

## Client and Project

<typed relations>

## External Authority

<Lexware pointer and last verified state>

## Evidence

<delivery and payment evidence>

## Timeline

- **<date>** | Invoice created or materially changed.
```

## Usage

Ausgangsrechnungen liegen lesbar in Lower Kebab Case unter `finance/rechnungen/`; die externe ID ist Relation, nicht Dateiidentität.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
