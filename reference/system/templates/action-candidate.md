---
schema_version: pos-v1
id: 019ff139-ac3d-7899-b5fb-c97c1f0e2234
type: template
title: "Template: Action Candidate"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/operations/action-und-attention-modell]]"]
target_profile_key: action-candidate
---

# Template: Action Candidate

## Template Contract

Normative Instanzvorlage für einen kurzlebigen Prüfzustand, wenn ein Signal möglicherweise handlungsrelevant ist, aber noch kein bestätigtes Commitment erzeugt.

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
evidence_refs: <evidence_refs>
---

# <title>

## Current Truth

<current_truth>

## Candidate Assessment

<candidate_assessment>

## Promotion Gate

<promotion_gate>

## Context and Evidence

<context_and_evidence>

## Timeline

- **<date>** | Action Candidate created.
```

## Usage

Nur als begrenztes Staging verwenden. Der Record wird zu Action, Trigger, Merge, Discard oder Ask disponiert und erscheint nie in normalen Action-Abfragen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
