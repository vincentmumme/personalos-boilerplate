---
schema_version: pos-v1
id: 019ffb7e-ebc8-75e9-9b37-341952a9f85b
type: template
title: "Template: Product"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: product
---

# Template: Product

## Template Contract

Kanonischer Hauptrecord eines dauerhaften Business-Produkts.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: product
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

## Value and Capabilities
<value_and_capabilities>

## Product Lifecycle
<product_lifecycle>

## Relationships
<relationships>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Productwahrheit, nicht Delivery Project, Repository oder einzelnes Offer.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
