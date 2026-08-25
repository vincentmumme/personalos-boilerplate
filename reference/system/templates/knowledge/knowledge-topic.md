---
schema_version: pos-v1
id: 01a0016e-6070-77e0-99de-872488ef98b8
type: template
title: "Template: Knowledge Topic"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
target_profile_key: knowledge-topic
---

# Template: Knowledge Topic

## Template Contract

Kanonischer Owner für Scope, Lifecycle und lokale Knowledge-Policy eines Topics. Der Record besitzt keine operative Wahrheit und keine vollständige Dateiliste.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-topic
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
---

# <title>

## Current Truth

<current topic identity and purpose>

## Scope

<included and excluded reusable knowledge>

## Ownership and Boundaries

<topic ownership and operative-truth boundary>

## Source and Compilation Policy

<source, maturity and compilation policy>

## Timeline

- **<date>** - <material change>
```

## Usage

Der Pfad lautet `knowledge/topics/<topic>/<topic>.md`. Archivierung ändert nur `lifecycle`; der Topic-Ordner bleibt im normalen Namespace.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
