---
schema_version: pos-v1
id: 019ffb8b-223d-7d7e-816d-ea31fb36ad8f
type: template
title: "Template: Brand Design System"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: brand-design-system
---

# Template: Brand Design System

## Template Contract

Kontrollierter visueller Companion eines existierenden Brand-Hauptrecords.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: brand-design-system
title: "<brand_name> Design System"
created: <date>
updated: <date>
lifecycle: active
canonical_system_ref: "<canonical_system_ref>"
authority_scope: <authority_scope>
brand_refs: <brand_refs>
---

# <brand_name> Design System

## Current Truth
<current_truth>

## Design Principles
<principles>

## Visual System
<visual_system>

## Components and Tokens
<components_and_tokens>

## Application
<application>

## Boundaries
<boundaries>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur unter `business/brands/<brand-slug>/design-system.md`. Physische Fonts, Logos, Bilder und Exporte bleiben im Asset-Layer.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
