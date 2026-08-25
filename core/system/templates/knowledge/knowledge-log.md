---
schema_version: pos-v1
id: 01a0016e-616a-740b-89a6-71c7fecdd0ad
type: template
title: "Template: Knowledge Log"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
target_profile_key: knowledge-log
---

# Template: Knowledge Log

## Template Contract

Append-only Verlauf materieller Knowledge-Aktionen auf Hub- oder Topic-Ebene. Der Log erklärt Veränderung, ersetzt aber weder Topic Truth noch Source oder Article.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-log
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
knowledge_log_scope: <knowledge_log_scope>
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
---

# <title>

## Entries

### <date> | <action>

<material change and provenance>

## Corrections

None.
```

## Usage

`topic_ref` ist bei Topic-Logs Pflicht und beim Hub-Log nicht gesetzt. Routine-No-ops werden nicht einzeln geloggt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
