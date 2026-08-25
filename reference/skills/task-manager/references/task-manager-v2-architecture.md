---
schema_version: pos-gbrain-v1
type: note
pos_domain: skills
role: reference
status: retired
title: "Task Manager v2 Architecture"
updated: 2026-08-11
tags: [task-management, operations, architecture, migration, retired]
---

# Task Manager v2 Architecture

> **Retired 2026-08-11:** Diese Datei beschreibt den Zwischenstand, in dem `operations/todo.md` noch als Blockliste weiterentwickelt werden sollte. Der atomare Action-/Attention-Cutover hat dieses Modell vollständig ersetzt.

## Current Owners

- Semantik und Zustandsmodell: [[system/frameworks/operations/action-und-attention-modell]]
- Kanonische Entscheidung: 2026 08 11 action und koordinationsmodell
- Ausführbarer Skill: [[skills/task-manager/SKILL]]
- Profile und Templates: [[system/data-model/index]], [[system/templates/action]], [[system/templates/attention-trigger]], [[system/templates/action-candidate]]
- Cutover-Beleg: action attention legacy todo dry run

## Compatibility Boundary

Alte Aussagen zu `operations/todo.md`, P0/P1/P2-Blöcken, `operations/tasks/`, Idea-Parked-Sektionen oder einer V3-Migration sind historische Migrationsannahmen und dürfen keine neuen Writes steuern. Aktive Actions liegen atomar unter `operations/actions/`; fällige Neubewertungen unter `operations/attention-triggers/`. `operations/todo.md` ist nur ein retired Kontinuitätszeiger.

## Timeline

- **2026-07-10** | Blocklistenbasierte V2-Zwischenarchitektur dokumentiert.
- **2026-08-11** | Nach erfolgreichem atomarem Action-/Attention-Cutover retired.
