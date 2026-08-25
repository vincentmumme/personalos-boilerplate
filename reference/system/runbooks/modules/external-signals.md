---
schema_version: pos-v1
id: "{{id_runbook_module_external_signals}}"
type: runbook
title: "Externe Signale verarbeiten"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Externe Signale verarbeiten

## Purpose

Externen Input nachvollziehbar in belastbaren PersonalOS-Kontext überführen.

## Trigger

Eine Nachricht, ein Call, eine E-Mail oder ein Feed enthält möglicherweise relevanten Kontext.

## Preconditions

Quelle, Zeitpunkt, Beteiligte und Datenschutzgrenze sind bekannt.

## Procedure

Quelle datenschutzgerecht erfassen oder referenzieren. Für einen lokalen Call [[skills/analyse-call/SKILL|analyse-call]] verwenden. Bei angebundenen Quellen zusätzlich Zugriff, Abrufgrenze und Fehlerverhalten dokumentieren. Erst danach Aussagen extrahieren, Unsicherheit markieren, Ziel-Owner bestimmen und Änderungen kontrolliert bestätigen.

## Verification

Input, Interpretation und übernommene Wahrheit bleiben unterscheidbar und rückverfolgbar.

## Escalation

Bei sensiblen Daten, unklarer Zustimmung oder widersprüchlichen Aussagen nicht automatisch übernehmen.

## Change History

- **{{install_date}}** | Modul aktiviert.
