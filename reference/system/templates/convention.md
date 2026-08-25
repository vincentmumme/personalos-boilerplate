---
schema_version: pos-v1
id: 019fec59-edb7-7f8c-a8cf-06b4125630b2
type: template
title: "Template: Convention"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: convention
---

# Template: Convention

## Template Contract

Instanzvorlage für einen konsistenten Default bei mehreren grundsätzlich zulässigen Ausprägungen.

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

## Convention

<convention>

## Use When

<use_when>

## Default

<default>

## Allowed Variations

<allowed_variations>

## Examples

<examples>

## Change History

- **<date>** | Convention created.
```

## Usage

Eine Abweichung braucht einen nachvollziehbaren Grund; echte Pflichten werden als Rule oder Contract modelliert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
