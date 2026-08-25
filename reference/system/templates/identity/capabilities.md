---
schema_version: pos-v1
id: 019ffb77-265c-74fd-a2b8-b2f1fcf2251a
type: template
title: "Template: Identity Capabilities"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-capabilities
---

# Template: Identity Capabilities

## Template Contract

Optionale Facette für dauerhaft belegbare Fähigkeiten, Erfahrung, Grenzen und Entwicklungsbezug.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-capabilities
title: "Capabilities"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Capabilities

## Current Truth
<current_truth>

## Capability Areas
<areas>

## Demonstrated Experience
<experience>

## Evidence and Credentials
<evidence>

## Limits
<limits>

## Related Development Projects
<project_links>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur materialisieren, wenn genug dauerhafte, belegbare Inhalte vorliegen. Keine leere Pflichtdatei und kein Ersatz für Projects oder Business-Positionierung.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
