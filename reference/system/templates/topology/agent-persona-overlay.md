---
schema_version: pos-v1
id: 019ffbfe-753d-71b5-a331-8e33d3dae608
type: template
title: "Template: Agent Persona Overlay"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: agent-persona-overlay
---

# Template: Agent Persona Overlay

## Template Contract

Normative Instanzvorlage für das registrierte `agent-persona-overlay`-Profil.

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
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: <authority_scope>
agent_ref: "<agent_ref>"
shared_persona_ref: "<shared_persona_ref>"
overlay_kind: <overlay_kind>
---

# <title>

## Current Truth

<current-truth>

## Inheritance

<inheritance>

## Behavior Additions

<behavior-additions>

## Communication

<communication>

## Boundaries

<boundaries>

## Sources

<sources>

## Timeline

<timeline>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
