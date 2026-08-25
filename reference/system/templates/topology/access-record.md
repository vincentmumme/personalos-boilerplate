---
schema_version: pos-v1
id: 019ffbfe-753d-7060-9c1d-5e4f335af675
type: template
title: "Template: Access Record"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: access-record
---

# Template: Access Record

## Template Contract

Normative Instanzvorlage für das registrierte `access-record`-Profil.

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
access_kind: <access_kind>
secret_owner: <secret_owner>
provisioning_state: <provisioning_state>
access_target_refs: <access_target_refs>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## Access Identity

<access-identity>

## Targets

<targets>

## Provisioning

<provisioning>

## Security Boundary

<security-boundary>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
