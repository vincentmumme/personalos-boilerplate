---
schema_version: pos-v1
id: "{{id_runbook_module_multi_agent}}"
type: runbook
title: "Mehrere Agenten koordinieren"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Mehrere Agenten koordinieren

## Purpose

Agentenarbeit teilen, ohne widersprüchliche Wahrheiten oder Schreibkonflikte zu erzeugen.

## Trigger

Eine Aufgabe soll von mehreren Agenten bearbeitet werden.

## Preconditions

Scope, Owner, Abhängigkeiten und Schreibflächen sind vorab geklärt.

## Procedure

Arbeit in unabhängige Einheiten zerlegen, Quellen mitgeben, Ergebnisse prüfen und nur kontrolliert in den kanonischen Owner übernehmen.

## Verification

Jede dauerhafte Aussage besitzt nach der Zusammenführung genau einen Owner und einen nachvollziehbaren Ursprung.

## Escalation

Bei überlappenden Schreibflächen oder widersprüchlichen Ergebnissen serialisieren und menschlich entscheiden.

## Change History

- **{{install_date}}** | Modul aktiviert.
