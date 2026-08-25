---
schema_version: pos-v1
id: 01a00193-cfdf-77fe-b3df-65e3597fb023
type: template
title: "Template: Health Operating Model"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-operating-model
---

# Template: Health Operating Model

## Template Contract

Kanonischer Operating-Model-Owner für die tatsächlich aktive Health-Architektur; keine zweite persönliche Health-Biografie und kein Provider-Runlog.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: health-operating-model
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<current operating model>

## Purpose

<questions the model answers>

## Active Data Flow

<provider to health truth flow>

## Active Object Model

<only actually used Health classes>

## Decision Logic

<calibration logic>

## Boundaries

<diagnostic, data and owner boundaries>

## Timeline

- **<date>** | Material operating-model change.
```

## Usage

Genau ein Record unter `health/healthos.md`. Neue Health-Klassen entstehen erst aus realer Nutzung und einem zugelassenen Profile.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
