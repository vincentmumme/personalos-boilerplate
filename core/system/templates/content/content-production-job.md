---
schema_version: pos-v1
id: 01a002b7-e000-7989-9264-3ce319c9364a
type: template
title: "Template: content-production-job"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-production-job
---

# Template: content-production-job

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-production-job` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-production-job"
title: "<title>"
created: "<date>"
updated: "<date>"
revision: <revision>
job_state: "<job_state>"
piece_ref: "<piece_ref>"
production_spec_ref: "<production_spec_ref>"
executor_type: "<executor_type>"
idempotency_key: "<idempotency_key>"
attempt: <attempt>
---

# <title>

## Summary

<summary>

## Evidence

<evidence>

## Corrections

<corrections>
```

## Usage

Use through the ContentOS skill. Structured payloads that do not drive routing or querying belong in the body or companion data.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
