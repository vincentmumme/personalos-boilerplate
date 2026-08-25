---
schema_version: pos-v1
id: 019ffb7e-ec54-7e51-a32d-0986cd0071df
type: template
title: "Template: Strategy"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: strategy
---

# Template: Strategy

## Template Contract

Kanonischer Hauptrecord einer geltenden Business-Strategie mit Choices, Trade-offs und Annahmen.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: strategy
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
canonical_system_ref: "<canonical_system_ref>"
authority_scope: <authority_scope>
---

# <title>

## Current Truth
<current_truth>

## Definition
<definition>

## Scope and Boundaries
<scope>

## Strategic Direction
<direction>

## Choices and Trade-offs
<choices>

## Assumptions and Measures
<assumptions_and_measures>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur angenommene Strategy Current Truth; Exploration und alternative Entwürfe bleiben im Project Working-Modul.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
