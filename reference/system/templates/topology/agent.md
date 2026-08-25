---
schema_version: pos-v1
id: 019ffbfe-753d-7f7d-b055-14df000a02b0
type: template
title: "Template: Agent"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: agent
---

# Template: Agent

## Template Contract

Normative Instanzvorlage für das registrierte `agent`-Profil.

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
agent_kind: <agent_kind>
agent_scope: <agent_scope>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## Scope and Responsibilities

<scope-responsibilities>

## Persona and Behavior

<persona-behavior>

## Runtime and Hosts

<runtime-hosts>

## Access and Boundaries

<access-boundaries>

## Sources

<sources>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
