---
schema_version: pos-v1
id: 01a001a0-f175-734c-86b6-49b704192339
type: template
title: "Template: Finance Payment Source Registry"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]"]
target_profile_key: finance-payment-source-registry
---

# Template: Finance Payment Source Registry

## Template Contract

Kanonische sichere Labels für Konten, Karten und andere Zahlungsquellen; keine Speicherung vollständiger Zahlungsinstrumente.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
registry_state: <registry_state>
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<current registry truth>

## Canonical Labels

<safe labels and scopes>

## Usage Rules

<selection and accounting rules>

## External Authority

<provider and accounting boundaries>

## Security Boundary

<forbidden identifiers and secret owner>

## Sources

<source map>

## Timeline

- **<date>** | Registry created or materially changed.
```

## Usage

Genau ein Record unter `finance/konten/payment-sources.md`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
