---
schema_version: pos-v1
id: 019ffb77-265c-75f1-9ffb-bf476b8f0f9a
type: template
title: "Template: Identity Biography"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-biography
---

# Template: Identity Biography

## Template Contract

Biografische Current Truth, Lebensphasen und prägende Ereignisse eines System-Subjects.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-biography
title: "Biografie"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Biografie

## Current Truth
<current_truth>

## Life Phases
<life_phases>

## Formative Events
<formative_events>

## Biography Gaps
<biography_gaps>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur dauerhafte biografische Wahrheit. Aktuelle Vorhaben bleiben Projects; Tagesereignisse bleiben Daily oder Evidence.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
