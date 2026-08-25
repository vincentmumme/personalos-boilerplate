---
schema_version: pos-v1
id: 01a02f99-806e-7121-887f-e0f3e4725351
type: automation
title: "Call Analysis Demo"
created: 2026-08-23
updated: 2026-08-23
lifecycle: planned
automation_kind: manual
---

# Call Analysis Demo

## Current Truth

Der Ablauf ist im Demo bewusst nur konzeptionell dokumentiert. Es gibt keine produktive Verbindung zu einem Kalender, Transkriptionsdienst oder echten Kundendaten.

## Purpose

Zeigen, wie aus einer neuen Gesprächsquelle Evidence, Analyse, propagierter Kontext und kontrollierte Actions entstehen können.

## Trigger and Cadence

Manueller Start mit einer ausgewählten, bereits redigierten Demo-Quelle.

## Capability and Runtime

Ein passender Call-Analyse-Skill kann von Codex oder Hermes ausgeführt werden. Die allgemeine Systemlogik bleibt unter [[system/index]].

## Inputs and Outputs

Input ist eine freigegebene Gesprächsquelle. Outputs sind Interaction Evidence, eine Analysis und gezielte Änderungen an den zuständigen Ownern. Ein möglicher Ablauf ist unter [[interactions/meetings/2026/2026-08-19-nordlicht-erstgespraech/2026-08-19-nordlicht-erstgespraech]] sichtbar.

## Credentials Required

Für die Demo keine. Produktive Connectoren würden separat eingerichtet und niemals mit Secret-Werten dokumentiert.

## Health and Freshness

Status `planned`: Das Demo zeigt die Architektur, führt aber keine externe Automation aus.

## Timeline

- **2026-08-23** | Konzeptionellen Demo-Ablauf angelegt.
