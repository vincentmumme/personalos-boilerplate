---
schema_version: pos-v1
id: 019ffb7e-eb69-7df2-b551-798fcafcb5dc
type: template
title: "Template: Market"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: market
---

# Template: Market

## Template Contract

Kanonischer Hauptrecord eines adressierten oder untersuchten Business-Markts.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: market
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

## Market Dynamics
<dynamics>

## Evidence and Assumptions
<evidence_and_assumptions>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Für fortlaufende Marktwahrheit; konkrete Research-Arbeit kann in Projects oder Knowledge entstehen und wird nach Annahme propagiert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
