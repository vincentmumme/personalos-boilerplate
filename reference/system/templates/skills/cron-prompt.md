---
schema_version: pos-v1
id: 01a00110-1fbf-7849-935e-9e8b81d4082b
type: template
title: "Template: Skill Cron Prompt"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/normative-system-architecture]]"]
target_profile_key: skill-prompt
---

# Template: Skill Cron Prompt

## Template Contract

Instanzvorlage für den bindenden, skilllokalen Ausführungsprompt eines geplanten Skills. Das Zielprofil besitzt Foundation, Lifecycle, normative Abhängigkeiten und die Relation zum ausführenden Skill; konkrete Schedule-, Runtime-, Verfahrens- und Delivery-Inhalte bleiben beim Skill.

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
decision_refs: <decision_refs>
system_refs: <system_refs>
invokes_skill_refs: <invokes_skill_refs>
---

# <title>

## Purpose

<purpose>

## Trigger

<trigger>

## Preconditions

<preconditions>

## Procedure

<procedure>

## Verification

<verification>

## Delivery

<delivery>
```

## Usage

Der Prompt liegt ausschließlich als `skills/<skill>/cron-prompt.md` beim ausführenden Skill und referenziert dessen `SKILL.md` über `invokes_skill_refs`. Allgemeine Regeln, Record-Shapes und Templates werden nicht lokal dupliziert, sondern über `system_refs`, Profile und gegebenenfalls `template_refs` geladen. Die Body-Struktur darf dem Job folgen; die sechs Blueprint-Abschnitte sind der bevorzugte Ausgangspunkt, keine starre globale H2-Schablone.

Ein Prompt mit `writes_profile_keys` deklariert zusätzlich die ausführbaren `check_refs`. Pausierte Jobs bleiben als `lifecycle: paused` lesbar, aber nicht ausführbar. Runtime-spezifische Pfade und Befehle dürfen im Body stehen, sofern sie den skilllokalen Job beschreiben und keine allgemeine PersonalOS-Norm beanspruchen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
