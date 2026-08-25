---
schema_version: pos-v1
id: 01a002b7-e000-75d7-a0d4-27fd5bfdafd4
type: template
title: "Template: content-version"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-version
---

# Template: content-version

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-version` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-version"
title: "<title>"
created: "<date>"
updated: "<date>"
lifecycle: "<lifecycle>"
revision: <revision>
piece_ref: "<piece_ref>"
platform: "<platform>"
publishing_account_key: "<publishing_account_key>"
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
