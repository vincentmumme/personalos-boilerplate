---
schema_version: pos-v1
id: 019fec59-ee99-71f3-a9e1-e84593924c5e
type: template
title: "Template: Skill"
created: 2026-08-10
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]", "[[system/contracts/core/capability-interface]]"]
target_profile_key: skill
---

# Template: Skill

## Template Contract

Instanzvorlage für einen runtimekompatiblen Skill. `name` und `description` bilden den universellen Discovery-Vertrag. Die geschlossene `pos_*`-Namespace innerhalb von `metadata` trägt die POS-Record-Foundation; POS-Integrationsfelder werden nur bei einer tatsächlichen Schnittstelle ergänzt.

## Blueprint

```markdown
---
name: <name>
description: "<description>"
metadata:
  pos_schema_version: pos-v1
  pos_id: <id>
  pos_type: skill
  pos_title: "<title>"
  pos_created: "<date>"
  pos_updated: "<date>"
  pos_lifecycle: <lifecycle>
  pos_skill_version: <skill_version>
---

# <title>

## Purpose

<purpose>

## Workflow

<workflow>

## Resources

<resources>
```

## Usage

`name` entspricht dem Skillordner und wird nicht als `capability_key` dupliziert. Die POS-Foundation ist innerhalb von `metadata` mit `pos_` präfixiert, damit Runtime-Felder und POS-Felder nicht kollidieren. Fremde Runtime-Namensräume dürfen ebenfalls unter `metadata` liegen; unbekannte `pos_*`-Felder bleiben verboten.

Optionale POS-Integration wird im selben `metadata`-Block über `pos_system_refs`, `pos_reads_profile_keys`, `pos_writes_profile_keys`, `pos_template_refs`, `pos_invokes_skill_refs` und `pos_check_refs` ausgedrückt. Ein Feld wird vollständig weggelassen, wenn die Schnittstelle nicht existiert. `pos_writes_profile_keys` erfordert `pos_check_refs`. Externe Seiteneffekte wie ein Tally-Formular sind keine POS-Record-Writes und werden nicht durch ein generisches `mutating`-Feld mit POS-Mutationen vermischt.

Die Body-Struktur folgt dem Job des Skills. Es gibt bewusst keine globale Pflichtliste von H2-Sections; `Purpose`, `Workflow` und `Resources` sind ein schlanker Startpunkt, keine zweite Runtime-Norm.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
