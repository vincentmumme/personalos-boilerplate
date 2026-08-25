---
schema_version: pos-v1
id: 019ffb77-265c-774d-b24b-b3eea54bb332
type: template
title: "Template: Life Orientation"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-life-orientation
---

# Template: Life Orientation

## Template Contract

Langfristige Lebensrichtung und dauerhafte Prioritäten ohne operative Project- oder Action-Wahrheit.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-life-orientation
title: "Life Orientation"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Life Orientation

## Current Truth
<current_truth>

## Desired Way of Life
<desired_life>

## Long-Term Directions
<directions>

## Enduring Priorities
<priorities>

## Non-Negotiables
<non_negotiables>

## Trade-offs
<trade_offs>

## Related Projects
<project_links>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Enduring Direction gehört hierher; konkrete Ergebnisse, Zeitpläne und Migrationsarbeit gehören in Projects.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
