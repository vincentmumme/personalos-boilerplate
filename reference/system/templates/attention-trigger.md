---
schema_version: pos-v1
id: 019ff139-ac10-7bc8-a561-681a7572c940
type: template
title: "Template: Attention Trigger"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/operations/action-und-attention-modell]]"]
target_profile_key: attention-trigger
---

# Template: Attention Trigger

## Template Contract

Normative Instanzvorlage für eine datierte oder ereignisgebundene Neubewertung ohne vorweggenommene Action.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
trigger_kind: <trigger_kind>
review_at: <review_at>
evidence_refs: <evidence_refs>
---

# <title>

## Current Truth

<current_truth>

## Trigger

<trigger>

## Reassessment Rule

<reassessment_rule>

## Context and Evidence

<context_and_evidence>

## Timeline

- **<date>** | Attention Trigger created.
```

## Usage

Für spätere Neubewertung verwenden, wenn heute noch keine Handlung besteht. Beim Auslösen den aktuellen Kontext neu lesen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
