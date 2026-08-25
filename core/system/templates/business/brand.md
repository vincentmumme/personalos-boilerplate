---
schema_version: pos-v1
id: 019ffb7e-eb3a-70b7-ba84-5f78a7105708
type: template
title: "Template: Brand"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: brand
---

# Template: Brand

## Template Contract

Kanonischer Hauptrecord einer Business Brand mit stabilem gemeinsamen Rahmen und brandspezifischem Kern.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: brand
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

## Identity and Promise
<identity_and_promise>

## Positioning and Expression
<positioning_and_expression>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Brand-Wahrheit, nicht Company-Stammdaten, Content-Produktion oder Project-Working-Truth.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
