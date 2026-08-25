---
schema_version: pos-v1
id: 019fec27-4cb0-7c9f-9238-7c96c951fe4d
type: truth-system
title: "PersonalOS"
created: 2026-08-10
updated: 2026-08-14
system_kind: personal-os
default_timezone: Europe/Berlin
---

# PersonalOS

## Current Truth

PersonalOS ist {{user_name}}s dauerhaftes persönliches Kontext-, Wahrheits- und Second-Brain-System. Es hält den gesamten für {{user_name}} und seine Agenten relevanten Kontext auf Wahrheitsebene, auch wenn Repositories, Binärassets, Secrets oder gemeinsam kanonische Wahrheiten physisch in anderen Systemen liegen.

Der aktuelle Instanz-Default für lokale Zeitsemantik ist `Europe/Berlin`. Er ist ein veränderbarer Fallback, keine historische oder zukünftige Universalzeitzone; [[system/rules/core/timezone-and-local-day-boundary]] besitzt die Auflösungsreihenfolge.

## Scope

PersonalOS besitzt {{user_name}}s persönliche Wahrheit, Systemmetawahrheit und die Pointer zu extern oder gemeinsam kanonischen Systemen. Es ist kein universeller physischer Dateispeicher, kein Secret Store und kein Ersatz für fachlich autorisierte externe Systeme.

## Authority

{{user_name}} ist die menschliche Letztinstanz für Regeln, Root-Level-Governance und bewusste Architekturentscheidungen. Agenten arbeiten innerhalb des dokumentierten Systemvertrags, der zentralen Registry und der zuständigen Skills. Eine Wahrheit besitzt genau einen kanonischen Owner; abgeleitete Sichten und Pointer dürfen keine zweite Wahrheit erzeugen.

## Interfaces

- Agenten beginnen über `AGENTS.md`, `INDEX.md`, `USER.md` und gegebenenfalls `SOUL.md`.
- Skills routen und operationalisieren zentrale Regeln, Profile und Templates, besitzen sie aber nicht doppelt.
- GitHub sichert den textuellen POS-Bestand; Syncthing verteilt den Arbeitsbestand zwischen autorisierten Hosts.
- Externe oder gemeinsame Truth Systems werden durch Authority-/Pointer-Verträge referenziert.

## Timeline

- **2026-08-09** | PersonalOS als vollständige persönliche Kontext- und Wahrheitsschicht bestätigt.
- **2026-08-10** | Der agentenunabhängige Systemvertrag, Single-Owner-Prinzip und `pos-v1`-Datenmodell wurden entschieden.
- **2026-08-10** | Dieser Truth-System-Record wurde als erster `pos-v1`-Systemowner materialisiert.
- **2026-08-14** | `Europe/Berlin` als aktuellen, veränderbaren Instanz-Default für lokale Zeitsemantik dokumentiert; Ereignis-, Aufenthalts- und Kalenderkontext bleiben vorrangig.
- **2026-08-14** | Den Default als registriertes Frontmatter-Feld und über den gemeinsamen Resolver `system/data-model/scripts/time_context.py` maschinenlesbar gemacht; aktive Writer dürfen ihn nicht mehr eigenständig duplizieren.
