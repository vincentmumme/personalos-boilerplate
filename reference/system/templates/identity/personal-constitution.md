---
schema_version: pos-v1
id: 019ffb77-265c-7245-8791-16872365101c
type: template
title: "Template: Personal Constitution"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-personal-constitution
---

# Template: Personal Constitution

## Template Contract

Dauerhafte Werte, persönliche Prinzipien, Überzeugungen und Grenzen eines System-Subjects.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-personal-constitution
title: "Personal Constitution"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Personal Constitution

## Current Truth
<current_truth>

## Values
<values>

## Personal Principles
<principles>

## Beliefs
<beliefs>

## Boundaries and Non-Negotiables
<boundaries>

## Internal Tensions
<tensions>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Für langfristige persönliche Verfassung; keine Agentenregeln und keine operative Aufgabenliste.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
