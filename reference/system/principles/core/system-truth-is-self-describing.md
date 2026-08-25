---
schema_version: pos-v1
id: 019ffbfb-5350-733f-a6a1-3fb944e6935b
type: principle
title: "Das System beschreibt sich selbst"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Das System beschreibt sich selbst

## Principle

Alle allgemeingültige Meta-Wahrheit über Aufbau, Regeln, Verträge, Templates, Capabilities, Agenten, Runtimes, Hosts, Services, Integrationen, Access und beobachteten Systemzustand lebt unter `system/` und ist aus wenigen Grundlagen ableitbar.

## Rationale

Jeder Agent und jede spätere PersonalOS-Instanz muss das System ohne verborgenes Chatwissen oder skilllokale Gegenverfassung korrekt verstehen können. Nur explizite, verlinkte und prüfbare Systemwahrheit ist portabel.

## Implications

- Root-Einstiege bleiben klein und routen nach `system/`.
- Skills führen Jobs aus und referenzieren Systemverträge; sie definieren keine parallelen POS-Normen.
- Beobachtete Runtime- und Servicezustände sind abgeleitete System-Observability, keine Operations-Wahrheit.
- Boilerplate und Content können später aus demselben universellen Standard abgeleitet werden, ohne {{user_name}}s Instanzdaten zu kopieren.

## Boundaries

Fachliche Wahrheit bleibt bei ihrer Domain. Runtime-Secrets bleiben im Secret Store. Repositories besitzen technische Implementierungsdetails. `system/` hält deren Verträge, Identitäten, Pointer und Systemrelevanz, nicht jede externe Datei oder jeden Rohlog.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
