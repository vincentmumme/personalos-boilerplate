---
schema_version: pos-v1
id: "{{id_runbook_module_claude_code}}"
type: runbook
title: "Claude Code mit dem PersonalOS verbinden"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Claude Code mit dem PersonalOS verbinden

## Purpose

Claude Code als austauschbaren Agenten an dieselbe Kontextwahrheit anbinden.

## Trigger

Claude Code soll im PersonalOS arbeiten.

## Preconditions

Der Agent kann den lokalen Ordner lesen und respektiert die Bootstrap-Reihenfolge.

## Procedure

Root-Kontext laden, Aufgabe planen, Owner bestimmen, kontrolliert ändern und den zuständigen Check ausführen.

## Verification

Werkzeugspezifische Hinweise widersprechen keiner Systemregel und erzeugen keine zweite Wahrheit.

## Escalation

Bei Abweichungen gilt die PersonalOS-Systemwahrheit, nicht eine duplizierte Adapterregel.

## Change History

- **{{install_date}}** | Modul aktiviert.
