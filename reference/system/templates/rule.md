---
schema_version: pos-v1
id: 019fec59-ed62-7f0e-ae58-cf25982e0dcc
type: template
title: "Template: Rule"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: rule
---

# Template: Rule

## Template Contract

Instanzvorlage für eine atomare bindende Pflicht, Erlaubnis oder ein Verbot.

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
---

# <title>

## Rule

<rule>

## Scope and Trigger

<scope_and_trigger>

## Required Behavior

<required_behavior>

## Exceptions

<exceptions>

## Verification

<verification>

## Change History

- **<date>** | Rule created.
```

## Usage

Nur verwenden, wenn ein Verhalten tatsächlich verpflichtend, erlaubt oder verboten ist.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
