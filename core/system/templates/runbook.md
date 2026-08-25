---
schema_version: pos-v1
id: 019fec59-ee45-708a-81a3-c252da331f11
type: template
title: "Template: Runbook"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: runbook
---

# Template: Runbook

## Template Contract

Instanzvorlage für eine triggergebundene Betriebsprozedur.

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
system_refs: <system_refs>
---

# <title>

## Purpose

<purpose>

## Trigger

<trigger>

## Preconditions

<preconditions>

## Procedure

<procedure>

## Verification

<verification>

## Escalation

<escalation>

## Change History

- **<date>** | Runbook created.
```

## Usage

Ein Runbook operationalisiert vorhandene Systemnormen und führt keine eigene allgemeine Semantik ein.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
