---
schema_version: pos-v1
id: 01a0016e-60ef-733b-b45e-a8bc2ad4356f
type: template
title: "Template: Knowledge Inventory Item"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
target_profile_key: knowledge-inventory-item
---

# Template: Knowledge Inventory Item

## Template Contract

Nachverfolgbarer, noch nicht evidenzfähiger Knowledge-Kandidat. Das Inventar ist weder Wissenswahrheit noch ein zweites Task-System.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-inventory-item
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
inventory_kind: <inventory_kind>
inventory_state: <inventory_state>
---

# <title>

## Current State

<current candidate state>

## Rationale

<why this belongs in the inventory>

## Handoff

<ingest, dataset, compile or no-op>

## Sources

<candidate provenance>

## Re-entry

<next review condition>
```

## Usage

Inventory wird nur bei Bedarf unter einem Topic angelegt. Konkrete persönliche Arbeit bleibt in Operations.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
