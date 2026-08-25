---
schema_version: pos-v1
id: 01a0018c-2c38-7276-9ef9-656c59158aaf
type: template
title: "Template: Health Daily Assessment"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/health/health-system-boundary]]"]
target_profile_key: health-daily-assessment
---

# Template: Health Daily Assessment

## Template Contract

Kompakte persönliche Tagesableitung aus Provider-Evidenz und späteren subjektiven Inputs. Sie ist der Health-Owner dieses Tageszustands, aber kein allgemeines Daily Log und keine Diagnose.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
assessment_date: <date>
readiness_band: <readiness_band>
training_recommendation: <training_recommendation>
provider_snapshot_ref: "[[health/whoop/<year>/<date>-whoop]]"
subject_ref: "[[identity/me]]"
---

# <title>

## Current Truth

<compact daily health state>

## Readiness

<evidence-based readiness summary>

## Training Guidance

<pragmatic guidance or unknown>

## Evidence

- <provider snapshot and optional subjective sources>

## Data Gaps

<missing or conflicting signals>

## Timeline

- **<date>** | Assessment created or materially corrected.
```

## Usage

Der Pfad ist `health/daily/<year>/YYYY-MM-DD-health.md`. Allgemeine Tageschronik bleibt unter `/daily`; konkrete Commitments bleiben unter `/operations`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
