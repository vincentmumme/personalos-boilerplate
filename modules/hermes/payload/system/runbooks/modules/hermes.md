---
schema_version: pos-v1
id: "{{id_runbook_module_hermes}}"
type: runbook
title: "Hermes sicher anbinden"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Hermes sicher anbinden

## Purpose

Hermes als optionale Laufzeit an die gemeinsame PersonalOS-Wahrheit anbinden.

## Trigger

Ein dauerhaft oder remote erreichbarer Agent wird benötigt.

## Preconditions

Kern und Synchronisation funktionieren; Schreibrechte und externe Wirkungen sind geklärt.

## Procedure

Zuerst lesend lokal testen, dann Pfade parametrisieren, Berechtigungen begrenzen und jede Automation separat freigeben.

## Verification

Hermes liest dieselben kanonischen Dateien und besitzt keine konkurrierende Memory-Schicht.

## Escalation

Bei Drift, fehlender Synchronisation oder unklaren Schreibrechten alle automatischen Läufe stoppen.

## Change History

- **{{install_date}}** | Modul aktiviert.
