---
schema_version: pos-v1
id: 01a00193-d05b-7a14-a3a0-1d2a148a2446
type: template
title: "Template: Health Measurement"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-measurement
---

# Template: Health Measurement

## Template Contract

Kanonischer Kontext und Verlauf einer tatsächlich genutzten Messklasse. Messwerte bleiben mit Zeitpunkt und Quelle im Body; Provider-Snapshots ersetzen keine stärkere manuelle Wahrheit.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: health-measurement
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
measurement_scope: <measurement_scope>
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<current measurement context>

## Measurement Policy

<source precedence and cadence>

## Current Measurements

<dated, sourced measurements or none>

## Sources

<source links>

## Timeline

- **<date>** | Material measurement change.
```

## Usage

Der heutige Body-Measurement-Owner liegt unter `health/body/measurements.md`. Einzelmessungen werden nur materialisiert, wenn reale Nutzung eine eigene Reihe rechtfertigt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
