---
schema_version: pos-v1
id: 01a002b7-e000-79b2-ba66-d8b127f9c15f
type: template
title: "Template: content-production-spec"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-production-spec
---

# Template: content-production-spec

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-production-spec` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-production-spec"
title: "<title>"
created: "<date>"
updated: "<date>"
lifecycle: "<lifecycle>"
revision: <revision>
piece_ref: "<piece_ref>"
---

# <title>

## Current Truth

<current_truth>

## Details

<details>

## Timeline

<timeline>
```

## Usage

Use through the ContentOS skill. Structured payloads that do not drive routing or querying belong in the body or companion data.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
