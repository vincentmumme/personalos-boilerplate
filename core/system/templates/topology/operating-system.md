---
schema_version: pos-v1
id: 019ffbfe-753d-7e68-b6d8-edf25f704851
type: template
title: "Template: Operating System"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: operating-system
---

# Template: Operating System

## Template Contract

Normative Instanzvorlage für das registrierte `operating-system`-Profil.

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
operating_system_kind: <operating_system_kind>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## Scope

<scope>

## Authority

<authority>

## Interfaces

<interfaces>

## Modules

<modules>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
