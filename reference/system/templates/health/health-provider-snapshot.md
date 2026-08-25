---
schema_version: pos-v1
id: 01a0018c-2c0e-7f8f-98cf-943fa857ff2e
type: template
title: "Template: Health Provider Snapshot"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-provider-snapshot
---

# Template: Health Provider Snapshot

## Template Contract

Zeitgebundene, normalisierte Provider-Evidenz. Abfragerelevante Zustandsfelder stehen im Frontmatter; Messwerte und Providerdetails bleiben im Body, damit die globale Foundation schlank bleibt.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
snapshot_date: <date>
captured_at: <captured_at>
snapshot_state: <snapshot_state>
source_system: <source_system>
subject_ref: "[[identity/me]]"
---

# <title>

## Snapshot Summary

<coverage and provider state>

## Metrics

<normalised measurements; missing values stay explicit>

## Workouts

<provider workout evidence or none>

## Body Measurement

<provider measurement context or none>

## Interpretation Boundary

<no diagnosis; provider signal is not the complete personal health truth>

## Sources

<provider and capture timestamp>

## Corrections

None.
```

## Usage

Der Pfad ist `health/whoop/<year>/YYYY-MM-DD-whoop.md`. Ein wiederholter Sync aktualisiert denselben Tag; Korrekturen bleiben im Body nachvollziehbar.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
