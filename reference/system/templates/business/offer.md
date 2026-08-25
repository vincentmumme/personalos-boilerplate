---
schema_version: pos-v1
id: 019ffb7e-ebf6-72a3-8bdc-817eaa1913d5
type: template
title: "Template: Offer"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: offer
---

# Template: Offer

## Template Contract

Kanonischer Hauptrecord eines wiederholbaren Business Offers.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: offer
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

## Buyer and Problem
<buyer_and_problem>

## Scope and Delivery
<delivery>

## Commercial Logic
<commercial_logic>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Wiederholbares Offer, nicht kundenspezifischer Deal, Proposal-Asset oder Delivery Project.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
