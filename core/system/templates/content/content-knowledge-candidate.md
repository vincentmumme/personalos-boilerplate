---
schema_version: pos-v1
id: 01a002b7-e000-7484-99b8-a755dbc8e71f
type: template
title: "Template: content-knowledge-candidate"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-knowledge-candidate
---

# Template: content-knowledge-candidate

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-knowledge-candidate` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-knowledge-candidate"
title: "<title>"
created: "<date>"
updated: "<date>"
revision: <revision>
candidate_state: "<candidate_state>"
candidate_class: "<candidate_class>"
---

# <title>

## Purpose

<purpose>

## Working Notes

<working_notes>
```

## Usage

Use through the ContentOS skill. Structured payloads that do not drive routing or querying belong in the body or companion data.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
