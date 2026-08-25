---
schema_version: pos-v1
id: 019ffb7e-ec24-703b-9df6-af71b2829595
type: template
title: "Template: Business Model"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: business-model
---

# Template: Business Model

## Template Contract

Kanonischer Hauptrecord eines Business-Modells und seiner Wert- und Erlöslogik.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: business-model
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

## Value Creation
<value_creation>

## Revenue and Economics
<revenue_and_economics>

## System and Constraints
<system_and_constraints>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Für das dauerhafte Modell; Finanztransaktionen und operative Planung besitzen andere Owner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
