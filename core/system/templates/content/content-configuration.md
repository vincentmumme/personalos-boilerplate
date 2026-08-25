---
schema_version: pos-v1
id: 01a002b7-e000-7f7c-b323-b2d381d6a6ec
type: template
title: "Template: content-configuration"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-configuration
---

# Template: content-configuration

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-configuration` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-configuration"
title: "<title>"
created: "<date>"
updated: "<date>"
lifecycle: "<lifecycle>"
revision: <revision>
configuration_kind: "<configuration_kind>"
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
