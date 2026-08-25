---
schema_version: pos-v1
id: "{{id_runbook_module_codex}}"
type: runbook
title: "Codex mit dem PersonalOS verbinden"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# Codex mit dem PersonalOS verbinden

## Purpose

Codex kontrolliert auf die gemeinsame Kontextschicht zugreifen lassen.

## Trigger

Codex soll im PersonalOS lesen oder arbeiten.

## Preconditions

Der Workspace zeigt auf den PersonalOS-Ordner und die Root-Bootstrap-Dateien sind vorhanden.

## Procedure

Zuerst AGENTS, INDEX, USER, SOUL und system/index lesen lassen; danach den zuständigen Owner und die passende Prüfung bestimmen.

## Verification

Codex nennt vor einer Änderung Quelle, Ziel-Owner und Verifikation.

## Escalation

Bei widersprüchlichem Kontext nicht raten, sondern den Owner prüfen oder den Nutzer fragen.

## Change History

- **{{install_date}}** | Modul aktiviert.
