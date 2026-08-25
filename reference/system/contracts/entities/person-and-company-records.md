---
schema_version: pos-v1
id: 019ffb82-bba6-7aef-adfa-cc4eb877ad1e
type: contract
title: "Person and Company Records"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Person and Company Records

## Contract

`people/` und `companies/` bleiben getrennte flache Entity-Roots. Jede Person und jede Company besitzt genau einen lesbar benannten Hauptrecord. Die Records halten Entity Current Truth, {{user_name}}s Beziehungskontext, relevante Rollen, Quellen, Timeline und eine klar als Navigation erkennbare Sicht auf verbundene Owner.

## Scope

Der Vertrag gilt für Personen außer dem menschlichen System-Subject sowie für externe und eigene Companies. Er gilt nicht für Identity, Business Objects, Projects, Actions, Interactions, Finance oder Assets.

## Invariants

1. {{user_name}} besitzt keinen parallelen vollständigen `person`-Record; sein Owner ist `identity/me.md`.
2. Ein People- oder Company-Record darf keine freien Companion Directories oder fachfremden Unterlagen ansammeln.
3. Person- und Company-Records behaupten nur die PersonalOS-eigene Beziehungssicht beziehungsweise belegte Entity-Fakten; fremde vollständige Wahrheit bleibt extern.
4. Tasks, Messages, Calls, Deals, Projects, Offers, Strategies und Finance-Wahrheit werden verlinkt, nicht kopiert.
5. Entity Home Pages dürfen verteilten Kontext navigieren; manuell gepflegte Schattenlisten sind keine zweite Current Truth.
6. Sensibler Kontext wird nur bei dauerhaftem persönlichem Nutzen und angemessener Privacy-Grenze gehalten.
7. Optionale Vertiefungen wie Kommunikationspräferenzen, Entscheidungsstil, Motivation, Business Model oder Risiken bleiben Body-Module innerhalb der registrierten Hauptsektionen. Sie sind weder Pflichtfelder noch Anlass für neue Companion-Strukturen.
8. Materielle Entity-Claims werden gemäß [[system/conventions/core/claim-nahe-quellenplatzierung]] direkt belegt; die `Sources`-Sektion ist ergänzende Source Map.

## Interfaces

- Person kann über `primary_company_ref` eine primäre Company verlinken.
- Company kann über `primary_contact_refs` zentrale bekannte Personen verlinken.
- Business Objects verwenden `company_refs`; inverse Company-Dossiers werden daraus abgeleitet.
- Interactions und Sources belegen Änderungen; fachliche Propagation aktualisiert anschließend den Entity Record.

## Compliance

Profile, Templates, Fixtures und Registry prüfen Pfad, Frontmatter und Body Shape. Die Bestandsmigration benötigt ein vollständiges Inventar einschließlich Sync-Konflikten, UUID-Zuweisung, Linkplan, Deduplizierung und Recovery-Beleg.

## Evolution

Neue Entity-Felder werden nur aufgenommen, wenn sie stabilen Routing-, Query- oder Relationsnutzen besitzen. Sonst bleibt Kontext im Body. Companion-Strukturen erfordern eine neue ausdrückliche Architekturentscheidung.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
