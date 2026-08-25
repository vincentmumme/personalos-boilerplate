---
schema_version: pos-v1
id: 01a00193-d009-7700-9448-0e313b93722a
type: template
title: "Template: Health Profile"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-profile
---

# Template: Health Profile

## Template Contract

Kanonische persönliche Health-Ausgangslage, Ziele, Grenzen und Coaching-Kalibrierung. Messreihen und konkrete Pläne bleiben eigene Owner.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: health-profile
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<current personal health context>

## Goals and Context

<durable goals and activity context>

## Constraints

<known constraints without diagnosis>

## Coaching Mode

<how agents should support>

## Open Calibration

<real unresolved questions>

## Timeline

- **<date>** | Material profile change.
```

## Usage

Genau ein persönlicher Health Profile Record unter `health/profile.md`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
