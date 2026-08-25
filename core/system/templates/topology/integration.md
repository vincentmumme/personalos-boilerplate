---
schema_version: pos-v1
id: 019ffbfe-753d-70d4-934c-7e23c8a30c26
type: template
title: "Template: Integration"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: integration
---

# Template: Integration

## Template Contract

Normative Instanzvorlage für das registrierte `integration`-Profil.

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
integration_kind: <integration_kind>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## External Boundary

<external-boundary>

## Data and Authority

<data-authority>

## Credentials Required

<credentials-required>

## Health

<health>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
