---
schema_version: pos-v1
id: 01a00193-d031-79ce-9dc1-e321c9f13993
type: template
title: "Template: Health Plan"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-plan
---

# Template: Health Plan

## Template Contract

Kanonischer, kalibrierbarer Health- oder Trainingsplan. Ein Plan ist keine Session, Messung oder Diagnose.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: health-plan
title: "<title>"
created: <date>
updated: <date>
plan_state: <plan_state>
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<current plan state>

## Plan

<current plan>

## Calibration Rules

<how evidence changes execution>

## Progression Boundary

<when the plan becomes more detailed>

## Sources

<health evidence and feedback>

## Timeline

- **<date>** | Material plan change.
```

## Usage

Der aktuelle Trainingsplan liegt unter `health/training/plan.md`; Session-Evidenz benötigt bei realer Nutzung ein eigenes Profile.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
