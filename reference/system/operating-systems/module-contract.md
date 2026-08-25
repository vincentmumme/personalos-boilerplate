---
schema_version: pos-v1
id: 01a00118-1721-747f-a82a-bcbc1fbac843
type: operating-system
title: "Operating System Module Contract"
created: 2026-08-02
updated: 2026-08-14
lifecycle: active
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: full
operating_system_kind: module-contract
---

# Operating System Module Contract

## Current Truth

Ein XOS ist ein begrenztes Operating-System-Modul, kein Ordnersuffix und kein Marketinglabel.

## Purpose

Die gemeinsame Admission-, Ownership- und Portabilitätsgrenze für ContentOS, BusinessOS, Agent OS und künftige XOS-Module festlegen.

## Scope

Ein zulässiges XOS definiert:

1. purpose and users;
2. host and dependencies;
3. canonical truth owners;
4. object and workflow contracts;
5. capability entry points;
6. knowledge dependencies;
7. operational data and evidence;
8. external provider boundary;
9. private instance configuration versus portable core;
10. lifecycle, validation and recovery.

## Authority

- The registry owns topology only. Domain contracts own domain logic.
- A module may reference another module's truth but cannot create a competing owner.
- Providers execute, store or measure; they do not become canonical architecture.
- Skills expose capabilities; they must obey domain contracts and templates.
- Instance-specific Brand, people, offers, credentials and accounts stay outside the portable core.
- A new module requires one comprehensible system map, one direct entry and deterministic validation.

## Interfaces

- Registry und index besitzen nur Topologie und Navigation.
- Domainverträge besitzen Objekt-, Workflow- und Wahrheitssemantik.
- Skills führen Capabilities aus; Provider speichern, veröffentlichen, routen oder messen.
- Externe und gemeinsame Truth Systems werden über Authority und Pointer verbunden.

## Modules

Ein Modul ist portabel, wenn Contracts, Templates und Workflows in einem anderen kompatiblen Host installiert werden können und Instanzkonfiguration separat geliefert wird. Fest codierte Personen, Maschinenpfade, Credentials oder Provider-IDs im portablen Core verletzen diesen Vertrag.

## Timeline

- **2026-08-02** | Gemeinsamen Modulvertrag für ContentOS und künftige XOS-Module angelegt.
- **2026-08-14** | In das registrierte Operating-System-Profil überführt und als gemeinsamer Modulvertrag typisiert.
