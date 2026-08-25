---
schema_version: pos-v1
id: 01a001a0-f19d-7f2c-9d78-b4f7e36ed4e9
type: template
title: "Template: Finance Expense"
created: 2026-08-14
updated: 2026-08-23
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-expense
---

# Template: Finance Expense

## Template Contract

Agentisch relevanter Zustand einer Ausgabe oder eines Eingangsbelegs; keine Parallelbuchhaltung zu Lexware.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
expense_date: <expense_date>
booking_state: <booking_state>
finance_scope: <finance_scope>
---

# <title>

## Current Truth

<current expense state>

## Expense

<vendor, description and monetary context>

## Booking and Payment State

<separate booking and payment truth>

## Allocation

<company, project or personal allocation>

## External Authority

<Lexware or other authority pointer>

## Evidence

<source and asset pointers>

### Receipt Package

| Feld | Wert |
|---|---|
| Originalbeleg | <asset, local intake source or external document pointer> |
| Tatsächlicher Abrufweg | <email, portal, API, upload or user-provided> |
| Zahlungsnachweis | <bank/card/private payment evidence or not-required> |
| Recurring-Owner | <link when stable provider logic exists; otherwise not-applicable> |
| Externe Buchung | <Lexware or other authority pointer and state> |
| Evidence-Lücke | <none or precise missing evidence> |

## Timeline

- **<date>** | Expense created or materially changed.
```

## Usage

Eingangsbelege liegen unter `finance/belege/`; interne Entity-Kosten unter `finance/entity-costs/` verwenden denselben fachlichen Expense-Owner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
