---
schema_version: pos-v1
id: 01a00126-9245-753c-ba1f-4fc5a907223e
type: template
title: "Template: Skill Resolver"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
target_profile_key: skill-resolver
---

# Template: Skill Resolver

## Template Contract

Instanzvorlage für den einen PersonalOS-weiten Intent-zu-Capability-Resolver. Der Resolver besitzt ausschließlich Routing und lädt die kanonische `SKILL.md`; allgemeine Systemregeln, Skilllogik und fachliche Wahrheit bleiben bei ihren jeweiligen Ownern.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
---

# <title>

## Purpose

<purpose>

## Routes

<intent-to-capability routes>

## Routing Rules

<selection, chaining and ambiguity rules>

## Maintenance

<verification and evolution rules>
```

## Usage

Es existiert genau ein Record am stabilen Pfad `skills/RESOLVER.md`. Fachliche Gruppen werden als H3 unter `Routes` organisiert, damit neue Skills ohne Profiländerung eingeordnet werden können. Der Resolver dupliziert weder Skillverträge noch Systemnormen und wird nach jeder Änderung durch den Control-Plane-Check verifiziert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
