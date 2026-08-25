---
schema_version: pos-v1
id: 01a00118-16f7-7ea0-b9b5-a45b9d78780c
type: operating-system
title: "PersonalOS"
created: 2026-08-02
updated: 2026-08-14
lifecycle: active
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: full
operating_system_kind: personal-os
---

# PersonalOS

## Current Truth

PersonalOS ist {{user_name}}s dauerhaftes privates Kontext-, Wahrheits- und Second-Brain-System. Es hält die für {{user_name}} und seine Agenten relevante Wahrheit auf Markdown-Ebene und kennt externe Owner, Repositories, Assets und Secrets über klare Grenzen und Pointer.

## Purpose

{{user_name}}s gesamten nutzbaren Lebens-, Business-, Arbeits- und Systemkontext so strukturieren, dass unterschiedliche Agenten und Runtimes zuverlässig damit arbeiten können.

## Scope

PersonalOS besitzt persönliche Wahrheit, Systemmetawahrheit, Navigation, Operations und die im Rootmodell zugelassenen Domains. Es ist kein Binärasset-Speicher, kein Secret Store, kein Repository-Container und kein Ersatz für ausdrücklich autorisierte gemeinsame oder externe Truth Systems.

## Authority

Der kanonische Authority-Vertrag liegt in [[system/truth-systems/personalos]]. {{user_name}} ist menschliche Letztinstanz; `/system` besitzt die allgemeine Systemsemantik, fachliche Roots besitzen ihre Domainwahrheit und Skills führen innerhalb dieser Verträge aus.

## Interfaces

- [[AGENTS]], [[INDEX]], [[USER]] und [[SOUL]] bilden den gemeinsamen Bootstrap.
- GitHub sichert die textuelle Wahrheit; Syncthing verteilt den Arbeitsbestand zwischen autorisierten Hosts.
- 1Password beziehungsweise lokale Runtime Stores besitzen Secret-Werte.
- Repositories, Assets und externe Wahrheiten bleiben bei ihren Ownern und werden über Pointer eingebunden.

## Modules

- contentos ist heute aktiv im PersonalOS gehostet.
- businessos bleibt geplant und besitzt noch keine eigene gemeinsame Wahrheitsschicht.
- aios ist die übergeordnete Kategorie, kein zusätzlicher Datenowner.

## Timeline

- **2026-08-02** | PersonalOS als aktueller Host für ContentOS und BusinessOS-Kontext registriert.
- **2026-08-14** | In das Operating-System-Profil überführt und mit dem kanonischen PersonalOS-Truth-System verbunden.
