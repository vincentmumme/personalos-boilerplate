---
schema_version: pos-v1
id: "{{id_skills_index}}"
type: owner-index
title: "Skills"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Skills

## Purpose

`skills/` enthält ausführbare Fähigkeiten. Allgemeine Regeln, Verträge, Frameworks und Templates bleiben unter [[system/index]].

## Ownership and Boundaries

Skills besitzen ihre konkrete Ausführung. Systemweite Normen und persistierte Record-Formate bleiben unter [[system/index]].

## Navigation

- [[skills/pos-verify/SKILL|pos-verify]] – Änderungen am PersonalOS prüfen
- [[skills/task-manager/SKILL|task-manager]] – Actions und Aufmerksamkeit verwalten
- [[skills/priority-dashboard/SKILL|priority-dashboard]] – eine ableitbare Prioritätssicht erzeugen
- [[skills/log/SKILL|log]] – dauerhaften Kontext aus einer Session sichern
- [[skills/skillify/SKILL|skillify]] – wiederkehrende Abläufe als Skill bewerten
- [[skills/write-skill/SKILL|write-skill]] – neue Skills kontrolliert anlegen
- [[skills/analyse-call/SKILL|analyse-call]] – lokale Call-Belege nachvollziehbar in Kontext überführen

Optionale Fähigkeiten werden als Module installiert und anschließend in [[skills/RESOLVER]] geroutet. Verbindungen zu externen Quellen bleiben unabhängig von der lokalen Analysefähigkeit optional.

## Maintenance

Der Index zeigt nur stabile Fähigkeiten. Auswahlregeln gehören ausschließlich in [[skills/RESOLVER]].
