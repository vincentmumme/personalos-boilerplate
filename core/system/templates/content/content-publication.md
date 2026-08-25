---
schema_version: pos-v1
id: 01a002b7-e000-7b76-b3a6-22a631d53cd2
type: template
title: "Template: content-publication"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-publication
---

# Template: content-publication

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-publication` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-publication"
title: "<title>"
created: "<date>"
updated: "<date>"
revision: <revision>
publication_state: "<publication_state>"
piece_ref: "<piece_ref>"
version_ref: "<version_ref>"
platform: "<platform>"
publishing_account_key: "<publishing_account_key>"
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
