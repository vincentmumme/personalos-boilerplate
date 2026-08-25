---
schema_version: pos-v1
id: 019ff59c-3127-79ee-bc94-0a9c21b1044b
type: template
title: "Template: Interaction Analysis"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
target_profile_key: interaction-analysis
---

# Template: Interaction Analysis

## Template Contract

Nicht-kanonische, quellennah bleibende Analyse von Interaction Evidence einschließlich Widersprüchen, Unsicherheit und Propagation.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
analysis_kind: <analysis_kind>
analysis_outcome: <analysis_outcome>
interaction_ref: "<interaction_ref>"
evidence_refs: <evidence_refs>
affected_owner_refs: <affected_owner_refs>
---

# <title>

## Analysis

<source-bounded interpretation>

## Findings

<material findings>

## Contradictions and Uncertainty

<conflicts, confidence boundaries or none>

## Propagation

<update, reference, no-op, stage and ask decisions>

## Sources

<evidence links>

## Corrections

None.
```

## Usage

Semantic Analysis, interaction-spezifisches Research und kombinierte Analysen nutzen dasselbe Profile mit explizitem `analysis_kind`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
