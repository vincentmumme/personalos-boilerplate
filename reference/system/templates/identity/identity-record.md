---
schema_version: pos-v1
id: 019ffb77-265c-7e03-a130-08c6657175bf
type: template
title: "Template: Identity Record"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-record
---

# Template: Identity Record

## Template Contract

Portabler kanonischer Hauptrecord eines menschlichen System-Subjects. Details werden nicht dupliziert, sondern über standardisierte Facetten navigiert.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-record
title: "<subject_display_name>"
created: <date>
updated: <date>
lifecycle: active
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: full
---

# <subject_display_name>

## Current Truth

<current_truth>

## Core Identity

<core_identity>

## Identity Facets

<facet_navigation>

## Connected Context

<connected_context>

## Sources

<sources>

## Timeline

- **<date>** | Record created.
```

## Usage

Genau ein Hauptrecord pro PersonalOS-Instanz. Keine zweite vollständige Personendatei unter `people/` und keine Project-, Business- oder Legal-Detailwahrheit im Hauptrecord.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
