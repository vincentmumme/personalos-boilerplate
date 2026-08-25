---
schema_version: pos-v1
id: 019ffbfe-753d-7e0e-b027-646600a9ed0a
type: template
title: "Template: Runtime"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: runtime
---

# Template: Runtime

## Template Contract

Normative Instanzvorlage für das registrierte `runtime`-Profil.

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
runtime_kind: <runtime_kind>
agent_refs: <agent_refs>
host_refs: <host_refs>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## Agents

<agents>

## Hosts and Execution

<hosts-execution>

## Configuration

<configuration>

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
