---
schema_version: pos-v1
id: 019fec59-ee71-7866-970c-cc09867ce4f0
type: template
title: "Template: Check"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: check
---

# Template: Check

## Template Contract

Instanzvorlage für die deklarative Seite einer deterministischen Systemprüfung.

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
check_kind: <check_kind>
verifies_refs: <verifies_refs>
---

# <title>

## Purpose

<purpose>

## Assertions

<assertions>

## Implementation

<implementation>

## Invocation

<invocation>

## Outcomes

<outcomes>

## Change History

- **<date>** | Check created.
```

## Usage

Der Check verweist auf bestehende Normen; Code und Ergebnisse dürfen keine neue Norm erzeugen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
