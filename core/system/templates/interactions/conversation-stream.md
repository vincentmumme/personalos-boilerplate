---
schema_version: pos-v1
id: 019ff59c-30cd-711f-9386-f8308adc5ccd
type: template
title: "Template: Conversation Stream"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]"]
target_profile_key: conversation-stream
---

# Template: Conversation Stream

## Template Contract

Kanonischer Record eines fortlaufenden Kommunikationsstroms. Current Truth ist ausschließlich auf Kanal, Beteiligte, Coverage, letzte materielle Kommunikationsentwicklung und Quellenlücken begrenzt.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
stream_state: <stream_state>
source_channel: <source_channel>
participant_refs: <participant_refs>
---

# <title>

## Current Truth

<current interaction context only>

## Participants

<participant links and roles>

## Coverage

<covered window and evidence pointers>

## Open Source Gaps

<missing media, unresolved mapping or none>

## Owner Links

<canonical people, company, project, operations and domain owners>

## Timeline

- **<date>** | Conversation stream created.
```

## Usage

Der Zielpfad bleibt `interactions/conversations/<channel>/<stream-slug>/conversation.md`. Fachliche Wahrheit und Aufgaben werden nur verlinkt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
