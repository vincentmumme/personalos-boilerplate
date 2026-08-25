---
schema_version: pos-v1
id: 01a001a0-f295-7acc-99b1-afe7ba1a6a49
type: template
title: "Template: Finance Tax Manifest"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/finance/finance-system-boundary]]", "[[system/contracts/core/file-and-asset-boundary]]"]
target_profile_key: finance-tax-manifest
---

# Template: Finance Tax Manifest

## Template Contract

Nachvollziehbares Quellen- und Integritätsmanifest eines Steuerjahres; keine zweite Dossierwahrheit und keine Binärablage.

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
manifest_state: <manifest_state>
tax_dossier_ref: "[[examples/tax-dossier]]"
---

# <title>

## Current Truth

<manifest coverage truth>

## Scope

<source boundary>

## Source Inventory

<asset pointers and source roles>

## Integrity

<hash and verification state>

## Missing Sources

<explicit gaps>

## Dossier Relation

<canonical dossier owner>

## Timeline

- **<date>** | Manifest created or materially changed.
```

## Usage

Genau ein `manifest.md` je materialisiertem Steuerjahr.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
