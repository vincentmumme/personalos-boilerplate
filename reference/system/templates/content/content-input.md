---
schema_version: pos-v1
id: 01a002b7-e000-7625-a93b-b2806e2b13ed
type: template
title: "Template: content-input"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-input
---

# Template: content-input

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-input` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-input"
title: "<title>"
created: "<date>"
updated: "<date>"
revision: <revision>
content_captured_at: "<content_captured_at>"
routing_decision: "<routing_decision>"
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
