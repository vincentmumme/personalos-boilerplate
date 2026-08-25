---
schema_version: pos-v1
id: 01a002b7-e000-79d1-b94f-a91fec7941c0
type: template
title: "Template: content-tracking-link"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-tracking-link
---

# Template: content-tracking-link

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-tracking-link` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-tracking-link"
title: "<title>"
created: "<date>"
updated: "<date>"
revision: <revision>
link_state: "<link_state>"
piece_ref: "<piece_ref>"
channel_key: "<channel_key>"
placement: "<placement>"
destination_url: "<destination_url>"
provider_key: "<provider_key>"
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
