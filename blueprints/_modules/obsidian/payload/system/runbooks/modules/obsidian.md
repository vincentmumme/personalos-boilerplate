---
schema_version: pos-v1
id: "{{id_runbook_module_obsidian}}"
type: runbook
title: "Obsidian als Oberfläche verbinden"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Obsidian als Oberfläche verbinden

## Purpose

Den PersonalOS-Ordner in Obsidian sichtbar machen, ohne eine zweite Wahrheit zu erzeugen.

## Trigger

Obsidian soll als Editor und Navigator genutzt werden.

## Preconditions

Der Kern funktioniert bereits als normaler lokaler Ordner.

## Procedure

Eine Kopie als Vault öffnen, Links prüfen und Plugins nur einzeln nach echtem Bedarf ergänzen.

## Verification

Dateien bleiben außerhalb von Obsidian lesbar und Agenten greifen auf denselben Ordner zu.

## Escalation

Bei Plugin-Abhängigkeiten zuerst prüfen, ob die Funktion mit Markdown und vorhandenen Regeln lösbar ist.

## Change History

- **{{install_date}}** | Modul aktiviert.
