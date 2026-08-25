---
schema_version: pos-v1
id: "{{id_skill_resolver}}"
type: skill-resolver
title: "Skill Resolver"
created: "{{install_date}}"
updated: "{{install_date}}"
---

# Skill Resolver

## Purpose

Dieser Record ordnet einen klaren Intent der passenden ausführbaren Fähigkeit zu.

## Routes

| Intent | Skill |
|---|---|
| PersonalOS-Dateien wurden erstellt, geändert, verschoben oder gelöscht | [[skills/pos-verify/SKILL|pos-verify]] |
| Action, Task, Waiting, Blocker oder Attention Trigger verwalten | [[skills/task-manager/SKILL|task-manager]] |
| Prioritäten-Dashboard ableiten, erklären oder aktualisieren | [[skills/priority-dashboard/SKILL|priority-dashboard]] |
| Session-Ergebnis oder Reflexion dauerhaft sichern | [[skills/log/SKILL|log]] |
| Wiederkehrenden Ablauf auf Skill-Eignung prüfen | [[skills/skillify/SKILL|skillify]] |
| Einen neuen PersonalOS-Skill anlegen oder ändern | [[skills/write-skill/SKILL|write-skill]] |
| Lokalen Call oder Meeting-Beleg analysieren und in Kontext überführen | [[skills/analyse-call/SKILL|analyse-call]] |

## Routing Rules

1. Der spezifischste passende Skill gewinnt.
2. Skills führen aus, aber besitzen keine konkurrierende allgemeine Systemlogik.
3. Ohne klare Route wird zuerst [[system/frameworks/core/context-routing-and-truth-propagation]] angewendet.
4. Mutierende Skills folgen dem zentralen Mutation Contract und enden mit `pos-verify`.
5. [[system/runbooks/modules/index]] zeigt die installierten Domain-, Werkzeug- und Infrastrukturmodule. Modulspezifische Fähigkeiten werden nur ergänzt, wenn sie eine echte ausführbare Route besitzen.

## Maintenance

Neue oder geänderte Skills werden hier nur ergänzt, wenn sich ihre Auswahlgrenze materiell ändert. Überlappende Routen werden vor der Freigabe aufgelöst und mit realistischen Nutzerformulierungen getestet.
