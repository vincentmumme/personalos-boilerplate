---
schema_version: pos-v1
id: 019ffbfe-753d-7aed-bff1-42ab71002b52
type: template
title: "Template: System Service"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: system-service
---

# Template: System Service

## Template Contract

Normative Instanzvorlage für das registrierte `system-service`-Profil.

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
service_kind: <service_kind>
execution_target_refs: <execution_target_refs>
desired_state: <desired_state>
---

# <title>

## Current Truth

<current-truth>

## Purpose

<purpose>

## Desired State

<desired-state>

## Execution Target

<execution-target>

## Trigger and Dependencies

<trigger-dependencies>

## Health

<health>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
