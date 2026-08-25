---
schema_version: pos-v1
id: 01a0016e-6119-7213-9783-5696abd51101
type: template
title: "Template: Knowledge Dataset"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
target_profile_key: knowledge-dataset
---

# Template: Knowledge Dataset

## Template Contract

Pointer auf große, externe, veränderliche, binäre, sensible oder abfrageorientierte Daten. Das PersonalOS hält den Kontext, nicht den Payload.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-dataset
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
dataset_kind: <dataset_kind>
source_locator: <source_locator>
---

# <title>

## Dataset Boundary

<what the dataset is and is not>

## Locations and Access

<non-secret locations and access notes>

## Schema and Query Notes

<formats, schema and useful queries>

## Provenance

<sources, checksums and licenses>

## Re-entry

<next profiling or review condition>
```

## Usage

Der Hauptrecord liegt unter `knowledge/topics/<topic>/datasets/<dataset>/manifest.md`; Samples und Query-Dateien sind Companion Data.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
