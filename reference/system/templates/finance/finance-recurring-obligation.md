---
schema_version: pos-v1
id: 01a001a0-f243-7fe3-9250-8a57b1bdbad4
type: template
title: "Template: Finance Recurring Obligation"
created: 2026-08-14
updated: 2026-08-23
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-recurring-obligation
---

# Template: Finance Recurring Obligation

## Template Contract

Fortlaufende finanzielle Verpflichtung mit getrennter Vertrags-, Fälligkeits-, Zahlungs- und Buchungssicht.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
obligation_state: <obligation_state>
finance_scope: <finance_scope>
cadence: <cadence>
---

# <title>

## Current Truth

<current obligation truth>

## Obligation

<provider, service and contractual context>

## Cadence and Due State

<cadence, due rule and next due date>

## Cost and Allocation

<amounts and business allocation>

## Payment Source

<safe registry label>

## External Authority

<provider and Lexware state>

## Evidence

<invoice and payment sources>

### Receipt Retrieval

| Feld | Wert |
|---|---|
| Belegquelle | <email, portal, static document, provider API or user-supplied> |
| Billing-Account | <safe account identifier; never password, token or recovery code> |
| Portal / Navigation | <portal URL and exact UI path> |
| E-Mail-Suchmuster | <sender, subject or mailbox query; `not-applicable` when none> |
| Erwarteter Zeitpunkt | <invoice/debit cadence or trigger> |
| Abrufweg | <download/API/XHR/manual generation steps> |
| Erforderliche Evidence | <invoice, EUR debit proof, contract, participants, etc.> |
| Automatisierungsgrad | <agent-autonomous, browser-login, authenticator-user-step, user-supplied, provider-auto-booked> |
| Auth-Abhängigkeit | <password manager, named mailbox, authenticator, none; no secrets> |
| Ablageziel | <asset or external-authority destination> |
| Buchungsbesonderheiten | <category, tax, allocation and payment handling> |
| Letzter verifizierter Zugriff | <date and result> |
| Offene Zugriffslücke | <none or precise unresolved gap> |

## Timeline

- **<date>** | Obligation created or materially changed.
```

## Usage

Stabile Verpflichtungen liegen unter `finance/recurring/`; eine einzelne Monatsrechnung bleibt Expense Evidence.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
