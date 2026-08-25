---
schema_version: pos-v1
id: 01a001a0-f26c-723c-9bf3-b5959416f1b8
type: template
title: "Template: Finance Tax Dossier"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]", "[[system/contracts/core/file-and-asset-boundary]]"]
target_profile_key: finance-tax-dossier
---

# Template: Finance Tax Dossier

## Template Contract

Kanonischer aktueller Steuerkontext eines Jahres; externe Abgabe- und Bescheidssysteme bleiben Authority.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
tax_year: "<tax_year>"
filing_state: <filing_state>
---

# <title>

## Current Truth

<current tax-year truth>

## Filing Scope

<returns and periods>

## Filing State

<preparation, filed, assessed or closed>

## Tax Context

<relevant sourced facts>

## Documents and Evidence

<asset and manifest pointers>

## External Authority

<submission and assessment systems>

## Open Assessment

<open factual outcome, not tasks>

## Timeline

- **<date>** | Dossier created or materially changed.
```

## Usage

Ein Dossier pro Steuerjahr unter `finance/taxes/<year>/index.md`; Actions bleiben unter `/operations`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
