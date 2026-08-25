---
schema_version: pos-v1
id: 019ffbfe-753d-7658-9119-44a9b2451476
type: template
title: "Template: View Record"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: view-record
---

# Template: View Record

## Template Contract

Normative Instanzvorlage für das registrierte `view-record`-Profil.

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
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: <authority_scope>
view_kind: <view_kind>
derivation_mode: <derivation_mode>
source_owner_refs: <source_owner_refs>
---

# <title>

## Purpose

<purpose>

## Source Owners

<source-owners>

## Derivation

<derivation>

## Freshness

<freshness>

## Limitations

<limitations>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
