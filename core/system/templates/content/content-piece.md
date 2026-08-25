---
schema_version: pos-v1
id: 01a002b7-e000-7f0d-ae9d-84b95db1e7a8
type: template
title: "Template: content-piece"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-piece
---

# Template: content-piece

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-piece` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-piece"
title: "<title>"
created: "<date>"
updated: "<date>"
lifecycle: "<lifecycle>"
revision: <revision>
slug: "<slug>"
creation_mode: "<creation_mode>"
input_refs: <input_refs>
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
