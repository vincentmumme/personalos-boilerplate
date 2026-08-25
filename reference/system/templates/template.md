---
schema_version: pos-v1
id: 019fec59-ee19-764c-b575-a1021cbc6a07
type: template
title: "Template: Template"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: template
---

# Template: Template

## Template Contract

Selbstbeschreibende Instanzvorlage für einen normativen POS-Record-Blueprint.

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
target_profile_key: <target_profile_key>
---

# <title>

## Template Contract

<template_contract>

## Blueprint

<blueprint>

## Usage

<usage>

## Change History

- **<date>** | Template created.
```

## Usage

Templates wiederholen weder Felddefinitionen noch Enums; ihr Zielprofile bleibt der einzige Shape-Owner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
