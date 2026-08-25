---
schema_version: pos-v1
id: 01a0016e-609a-7517-9565-3b7bdec5b8f0
type: template
title: "Template: Knowledge Source"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]", "[[system/contracts/core/source-provenance]]"]
target_profile_key: knowledge-source
---

# Template: Knowledge Source

## Template Contract

Unveränderliche Rohquelle mit genau einem Topic-Owner. Korrekturen ergänzen die Evidenz, statt den ursprünglichen Source-Inhalt still umzuschreiben.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-source
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
knowledge_source_kind: <knowledge_source_kind>
source_locator: <source_locator>
captured_on: <date>
source_integrity: <source_integrity>
immutable: true
---

# <title>

## Source Summary

<summary>

## Routing

<primary topic and secondary relevance>

## Source Boundary

<origin, extraction path and trust boundary>

## Evidence

<preserved source content>

## Extraction Gaps

<gaps or None>

## Corrections

None.
```

## Usage

Source-Dateien liegen unter `knowledge/topics/<topic>/raw/<source-kind>/`. Große oder veränderliche Datensätze erhalten stattdessen einen Dataset-Manifest.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
