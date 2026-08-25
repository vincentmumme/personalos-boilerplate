---
schema_version: pos-v1
id: 01a001a0-f14d-756d-91ba-a7280f29228c
type: template
title: "Template: Finance Account"
created: 2026-08-14
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-account
---

# Template: Finance Account

## Template Contract

Kontext zu einem tatsächlich genutzten Finanzkonto. Verifizierte Bankkennungen dürfen hier stehen; Autorisierungs- und Zugangswerte bleiben im externen Secret Owner.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
account_state: <account_state>
finance_scope: <finance_scope>
institution: "<institution>"
subject_ref: "[[identity/me]]"
iban: "<iban-if-needed>"
bic: "<bic-if-needed>"
account_number: "<account-number-if-needed>"
---

# <title>

## Current Truth

<current account context>

## Purpose and Scope

<allowed use>

## Account Identity

<verified bank identity and identifiers needed for payment or reconciliation>

## Usage

<incoming, outgoing and accounting use>

## External Authority

<bank as external authority and optional secure locator for separate credentials>

## Security Boundary

<no card number, CVV/CVC, PIN, password, token, recovery code or online-banking credential>

## Sources

<evidence; never duplicate authorization or access secrets>

## Timeline

- **<date>** | Account context created or materially changed.
```

## Usage

Stabile Accounts liegen unter `finance/konten/`. Karten und PayPal-Labels gehören in die Payment Source Registry, nicht als erfundene Kontorecords.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
