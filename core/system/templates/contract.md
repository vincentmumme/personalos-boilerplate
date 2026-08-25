---
schema_version: pos-v1
id: 019fec59-ed8d-7a80-8d32-7f2b0d6c7379
type: template
title: "Template: Contract"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: contract
---

# Template: Contract

## Template Contract

Instanzvorlage für einen versionierten, zusammengesetzten und prüfbaren Systemvertrag.

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
decision_refs: <decision_refs>
contract_version: <contract_version>
---

# <title>

## Contract

<contract>

## Scope

<scope>

## Invariants

<invariants>

## Interfaces

<interfaces>

## Compliance

<compliance>

## Evolution

<evolution>

## Change History

- **<date>** | Contract created.
```

## Usage

Für zusammenhängende Interface-, Shape-, Ownership- oder Verhaltensverträge verwenden; atomare Pflichten bleiben Rules.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
