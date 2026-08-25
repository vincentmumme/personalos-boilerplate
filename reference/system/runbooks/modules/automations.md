---
schema_version: pos-v1
id: "{{id_runbook_module_automations}}"
type: runbook
title: "Automation sicher einführen"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Automation sicher einführen

## Purpose

Einen stabilen manuellen Ablauf kontrolliert automatisieren.

## Trigger

Ein Prozess ist wiederholt, verstanden und ausreichend stabil.

## Preconditions

Input, Output, Owner, Fehlerfälle, Berechtigungen und Verifikation sind dokumentiert.

## Procedure

Lesend beginnen, Dry Run einbauen, kleine Reichweite wählen, Ergebnisse protokollieren und Schreibrechte erst nach Prüfung aktivieren.

## Verification

Die Automation ist deterministisch prüfbar und kann ohne Datenverlust gestoppt werden.

## Escalation

Bei Drift, Fehlklassifikation oder ungeklärten externen Wirkungen sofort deaktivieren.

## Change History

- **{{install_date}}** | Modul aktiviert.
