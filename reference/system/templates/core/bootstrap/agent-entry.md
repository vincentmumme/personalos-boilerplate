---
schema_version: pos-v1
id: 019ffb24-1e28-7bcc-9f24-3182e936c8e1
type: template
title: "Template: Agent Entry"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]"]
target_profile_key: agent-entry-pointer
---

# Template: Agent Entry

## Template Contract

Portabler gemeinsamer PersonalOS-Bootstrap für alle Agenten einer Instanz. `<subject_display_name>` ist ein Pflichtplatzhalter des Instanzrenderings.

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
---

# <title>

Dies ist das PersonalOS von <subject_display_name>. Es ist die vollständige Markdown-basierte Kontext- und Wahrheitsschicht dieser Person.

## Verbindlicher Start

Lies vor der Arbeit im PersonalOS:

1. [[INDEX]] – Systemkarte, Navigation und kanonische Owner
2. [[USER]] – kompakter Kontext über das menschliche System-Subject
3. [[SOUL]] – gemeinsame Grundseele und Verhaltensbasis aller PersonalOS-Agenten
4. deine agentenspezifische Persona oder SOUL, sofern vorhanden – zusätzlich zur gemeinsamen Root-SOUL

## Arbeiten im PersonalOS

- [[skills/RESOLVER]] bestimmt die zuständige ausführbare Capability.
- [[system/index]] ist der Einstieg in alle Regeln, Verträge, Konventionen, Frameworks, Templates, Datenmodelle, Runbooks und Checks.
- Neue oder geänderte Records folgen dem registrierten Profil und Template unter [[system/data-model/index]].
- Mutationen folgen [[system/contracts/core/personalos-mutation-contract]] und enden mit der zuständigen Prüfung.
- Neue Root-Ordner, Profile, Felder oder Normen dürfen nicht improvisiert werden.

## Autorität

- `/system` besitzt die allgemeine PersonalOS-Systemwahrheit.
- Skills führen aus und dürfen keine konkurrierende Systemverfassung besitzen.
- Die Root-`SOUL.md` gilt gemeinsam mit einer zusätzlichen agentenspezifischen Persona.
- Bei einem echten Konflikt wird nicht still priorisiert, sondern der zuständige Owner geprüft oder das menschliche System-Subject gefragt.

Diese Datei ist ausschließlich Bootstrap und Pointer. Fachliche Wahrheit, Persona-Details und Systemregeln werden hier nicht dupliziert.
```

## Usage

Für `AGENTS.md` mit `entry_kind: common-bootstrap` rendern. Persönliche Angaben werden ausschließlich über deklarierte Instanzwerte eingesetzt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
