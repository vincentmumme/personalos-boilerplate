---
schema_version: pos-v1
id: 019ffb24-1e57-73fa-859e-19af68687e38
type: template
title: "Template: Claude Adapter"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]"]
target_profile_key: agent-entry-pointer
---

# Template: Claude Adapter

## Template Contract

Strikter technischer Adapter für Claude Code. Der gerenderte Body darf ausschließlich auf den gemeinsamen `AGENTS.md`-Bootstrap verweisen.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
entry_kind: <entry_kind>
bootstrap_ref: "<bootstrap_ref>"
---

# <title>

Lies vor jeder Arbeit in diesem PersonalOS [[AGENTS]] vollständig und folge dem dort definierten gemeinsamen Bootstrap.

Diese Datei ist ausschließlich ein technischer Pointer auf [[AGENTS]].
```

## Usage

Nur für `CLAUDE.md` mit `entry_kind: runtime-adapter` und `bootstrap_ref: "[[AGENTS]]"` rendern. Zusätzliche Abschnitte oder Anweisungen sind verboten.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
