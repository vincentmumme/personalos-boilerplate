---
schema_version: pos-v1
id: 019ffb82-bb5b-73f4-b59a-bd892b2d4c67
type: template
title: "Template: Company"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/entities/person-and-company-records]]"]
target_profile_key: company
---

# Template: Company

## Template Contract

Standardisierter flacher Company-Record als Entity Home Page ohne freien Company-Unterordner.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: company
title: "<company_name>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: <authority_scope>
---

# <company_name>

## Current Truth
<current_truth>

## Entity Facts
<entity_facts>

<!-- Optional, nur wenn materiell:
### Business Model
### Decision Logic
### Risks and Tensions
-->

## Relationship to Subject
<relationship>

## People and Roles
<people_and_roles>

## Connected Business Context
<business_links>

## Relevant Context
<context>

<!-- Optional, nur wenn materiell:
### Communication and Engagement Profile
### Open Threads
-->

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Company Entity Truth und abgeleitete Navigation halten. Optionale Module entstehen nur mit belegtem dauerhaftem Nutzen und bleiben innerhalb der bestehenden Sektionen. Materielle Claims werden claim-nah belegt; `Sources` bleibt ergänzende Übersicht. Brand, Market, Offer, Product, Strategy, Projects, Finance und Assets bleiben bei ihren Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
