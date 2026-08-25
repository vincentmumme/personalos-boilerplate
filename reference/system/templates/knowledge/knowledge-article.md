---
schema_version: pos-v1
id: 01a0016e-60c5-79df-a3aa-91553310ff0c
type: template
title: "Template: Knowledge Article"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]", "[[system/contracts/core/source-provenance]]"]
target_profile_key: knowledge-article
---

# Template: Knowledge Article

## Template Contract

Kompilierte, quellengebundene Wissenswahrheit eines Topics. Anwendung auf Personen, Unternehmen oder Projekte bleibt explizite Inferenz und erzeugt keine operative Zweitwahrheit.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-article
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
knowledge_article_kind: <knowledge_article_kind>
knowledge_maturity: <knowledge_maturity>
knowledge_confidence: <knowledge_confidence>
knowledge_volatility: <knowledge_volatility>
source_refs: ["[[knowledge/topics/<topic>/raw/<kind>/<source>]]"]
---

# <title>

## Current Knowledge

<source-grounded synthesis>

## Applicability Boundaries

<when it applies and when it does not>

## Sources

<resolvable source links>

## Timeline

- **<date>** - <material synthesis change>
```

## Usage

Artikel liegen unter `knowledge/topics/<topic>/wiki/<category>/`. `source_refs` wird nur gesetzt, wenn die Quellen bereits als Knowledge Source auflösbar sind.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
