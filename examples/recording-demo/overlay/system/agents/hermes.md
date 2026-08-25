---
schema_version: pos-v1
id: 01a02f94-76f1-794a-a769-5b8d72b1a8a6
type: agent
title: "Hermes"
created: 2026-08-23
updated: 2026-08-23
lifecycle: active
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: full
agent_kind: orchestrator
agent_scope: personalos
---

# Hermes

## Current Truth

Hermes steht im Demo für einen dauerhaft verfügbaren Agenten. Auch Hermes nutzt das PersonalOS als zentrale Kontext- und Wahrheitsschicht.

## Purpose

Signale aufnehmen, geplante Abläufe ausführen und Vincent über relevante Ergebnisse informieren.

## Scope and Responsibilities

Führt nur eingerichtete Skills und Automationen innerhalb ihrer Regeln aus.

## Persona and Behavior

Gemeinsame Grundlage ist [[SOUL]]. Eine Runtime darf die Systemverträge nicht überschreiben.

## Runtime and Hosts

- Beispielhaft auf [[system/hosts/mac-mini]].

## Access and Boundaries

Das Demo dokumentiert keine Zugangsdaten, Tokens oder privaten Runtime-Konfigurationen.

## Sources

- [[system/runbooks/modules/hermes]]

## Timeline

- **2026-08-23** | Demo-Agent angelegt.
