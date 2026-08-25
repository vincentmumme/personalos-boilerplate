---
schema_version: pos-v1
id: 01a002b7-e000-76ca-a634-1eadac6f60f3
type: template
title: "Template: content-research"
created: 2026-08-15
updated: 2026-08-15
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/content/object-model]]"]
target_profile_key: content-research
---

# Template: content-research

## Template Contract

Canonical POS-v1 blueprint for the ContentOS `content-research` primary profile.

## Blueprint

```markdown
---
schema_version: "pos-v1"
id: "<id>"
type: "content-research"
title: "<title>"
created: "<date>"
updated: "<date>"
lifecycle: "<lifecycle>"
revision: <revision>
research_question: "<research_question>"
source_refs: <source_refs>
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
