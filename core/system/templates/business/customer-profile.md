---
schema_version: pos-v1
id: 019ffb7e-eb99-75b7-bee5-767e83ad4a40
type: template
title: "Template: Customer Profile"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: customer-profile
---

# Template: Customer Profile

## Template Contract

Kanonischer Record eines ICP, einer Buyer-Klasse oder eines anderen stabilen Customer Profiles.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: customer-profile
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

## Target Customer
<target_customer>

## Problems and Desired Outcomes
<problems_and_outcomes>

## Qualification
<qualification>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Customer-Truth, nicht People-Record und nicht projektspezifische Stakeholderliste.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
