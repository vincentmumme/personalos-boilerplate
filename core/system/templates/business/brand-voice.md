---
schema_version: pos-v1
id: 019ffb8b-2210-72d5-893b-387f327ed623
type: template
title: "Template: Brand Voice"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/business/business-object-model]]"]
target_profile_key: brand-voice
---

# Template: Brand Voice

## Template Contract

Kontrollierter verbaler Companion eines existierenden Brand-Hauptrecords.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: brand-voice
title: "<brand_name> Tone of Voice"
created: <date>
updated: <date>
lifecycle: active
canonical_system_ref: "<canonical_system_ref>"
authority_scope: <authority_scope>
brand_refs: <brand_refs>
---

# <brand_name> Tone of Voice

## Current Truth
<current_truth>

## Voice Principles
<principles>

## Tone and Register
<tone_and_register>

## Language Patterns
<patterns>

## Boundaries
<boundaries>

## Application
<application>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Nur unter `business/brands/<brand-slug>/tone-of-voice.md` und nur gemeinsam mit dem gleichnamigen Brand-Hauptrecord.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
