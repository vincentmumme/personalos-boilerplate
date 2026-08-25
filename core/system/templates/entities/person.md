---
schema_version: pos-v1
id: 019ffb82-bb1d-7c58-acc7-a09b1994300c
type: template
title: "Template: Person"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/entities/person-and-company-records]]"]
target_profile_key: person
---

# Template: Person

## Template Contract

Standardisierter flacher Personenrecord für dauerhaften beziehungs- und arbeitsrelevanten Kontext im PersonalOS.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: person
title: "<full_name>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: personal-context
---

# <full_name>

## Current Truth
<current_truth>

## Identity and Roles
<identity_and_roles>

## Relationship to Subject
<relationship>

## Communication Profile
<communication>

<!-- Optional, nur bei belegtem dauerhaftem Nutzen:
### Preferred Communication
### Decision and Feedback Style
### Motivations and Drivers
-->

## Relevant Context
<context>

<!-- Optional, nur wenn materiell:
### What They Build
### Beliefs and Thinking
### Open Threads
-->

## Affiliations and Relationships
<affiliations>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur dauerhaften persönlichen Kontext halten. Optionale Module entstehen nur mit belegtem dauerhaftem Nutzen und bleiben innerhalb der bestehenden Sektionen. Materielle Claims werden claim-nah belegt; `Sources` bleibt ergänzende Übersicht. Tasks, Interactions, Projects und fremde private Vollprofile bleiben bei ihren Ownern; {{user_name}} selbst besitzt keinen parallelen People-Record.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
