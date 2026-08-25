---
schema_version: pos-v1
id: 019ff139-abe3-7dd2-a5a9-53a42c6346e6
type: template
title: "Template: Action"
created: 2026-08-11
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/operations/action-und-attention-modell]]"]
target_profile_key: action
---

# Template: Action

## Template Contract

Normative Instanzvorlage für ein bestätigtes persönliches Commitment. Feldregeln, Lifecycle und Timing-Semantik liegen im Registry-Profile.

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
execution_mode: <execution_mode>
evidence_refs: <evidence_refs>
affected_owner_refs: <affected_owner_refs>
---

# <title>

## Current Truth

<current_truth>

## Desired Outcome

<desired_outcome>

## Done Boundary

<done_boundary>

## Next Action

<next_action>

## Context and Evidence

<context_and_evidence>

## Timeline

- **<date>** | Action created.
```

## Usage

Nur für ein reales offenes Commitment verwenden. `evidence_refs` enthält ausschließlich Quellen und Belege. `affected_owner_refs` ist optional und verknüpft betroffene fachliche Owner wie Personen, Companies, Projects oder Business-Objekte. Waiting und Deferred sind Lifecycle-Zustände; Ideen und bloße Wiedervorlagen sind keine Actions.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
