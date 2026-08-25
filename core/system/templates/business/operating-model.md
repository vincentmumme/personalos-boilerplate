---
schema_version: pos-v1
id: 019ffb7e-ec84-73b8-bd92-e29e7c0ec810
type: template
title: "Template: Operating Model"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: operating-model
---

# Template: Operating Model

## Template Contract

Kanonischer Hauptrecord eines dauerhaften Business Operating Models.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: operating-model
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

## Operating Principles
<operating_principles>

## Roles and Responsibilities
<roles>

## Processes and Cadence
<processes_and_cadence>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Für wiederkehrende Betriebslogik; konkrete Actions, Run Receipts und Project Plans bleiben bei ihren Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
