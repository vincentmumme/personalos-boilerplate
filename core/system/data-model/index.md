---
schema_version: pos-v1
id: 01a00119-b08b-7d16-aff7-b9f7d433fdf6
type: owner-index
title: "PersonalOS Data Model"
created: 2026-08-06
updated: 2026-08-15
index_scope: section
---

# PersonalOS Data Model

## Purpose

Dieser Index führt Agenten und Maintainer zum maschinenlesbaren `pos-v1`-Datenmodell, seinen menschlich lesbaren Verträgen, generierten Artefakten, Templates, Checks und Migrationsgrenzen.

## Ownership and Boundaries

`registry.yaml` und seine referenzierten YAML-Dateien besitzen die maschinenlesbare Datenmodellwahrheit. Verträge und Frameworks erklären Semantik und Entscheidungen für Menschen. Generated Schemas und Indizes sind abgeleitete Artefakte; dieser Index besitzt weder Felddefinitionen noch Profile, Enums oder Migrationsstatus doppelt.

## Navigation

- [[system/data-model/frontmatter]] — gemeinsamer Kern und Profilgrenzen
- legacy mapping — Gbrain-/Legacy-Felder einordnen
- changelog — kontrollierte Änderungen
- [[system/data-model/governance]] — Admission, Activation, Deprecation und Evolution
- [[system/contracts/content/contentos-pos-v1-transition]] — historischer Beleg des am 2026-08-15 abgeschlossenen ContentOS-Domaincutovers
- [[system/contracts/identity/identity-subject-and-facets]] — Subject-Hauptrecord, Identity-Facetten und Ownergrenzen
- [[system/contracts/business/business-object-model]] — acht Business-Objektklassen, Relations und Companion-Grenze
- [[system/contracts/entities/person-and-company-records]] — standardisierte flache People-/Company-Records und Entity-View-Grenzen
- [[system/contracts/system/system-topology-and-access]] — Agenten, Runtimes, Hosts, Services, Access und Observability
- `registry.yaml` — kanonisches Pack-Manifest
- `foundation.yaml` — universeller Sechs-Feld-Vertrag
- `governance.yaml` und `deprecations.yaml` — maschinenlesbarer Governance- und Auslaufvertrag
- `page-shapes/` — geschlossene Body-Grundformen
- `modules/` — wiederverwendbare Feld- und Semantikowner
- `profiles/` — Primary Profiles mit Pfad-, Body- und Zustandsvertrag
- `scripts/pos_v1.py` — dependency-free Registry-Runtime für ID, Render und Verify
- `scripts/daily_records.py` — validierender Renderer für modulare Day Records und atomare Activity Contributions; Workflow-Ownership bleibt beim aufrufenden Skill
- `scripts/automation_records.py` — validierender, idempotenter Renderer für materielle Automation Receipts und kompakte Day Summaries nach Variante C; technischer Run-State bleibt beim Producer
- `processing-receipt` — gesonderter Interaction-Verarbeitungsbeleg für Multi-Owner-Propagation, Partial Failure oder Auditbedarf; nicht mit Source Evidence oder Analyse vermischen
- `signal-digest` — quellengebundene tägliche Verdichtung allgemeiner News-, Web- und Creator-Signale unter `/interactions`; Automation-Receipts und fachliche Owner bleiben getrennt
- `daily-briefing` — abgeleitete Entscheidungsvorlage im lokalen Daily-Container; Automation besitzt Trigger, Skill besitzt Verhalten und Delivery bleibt Side Effect
- `context-gap-review` — abgeleitete Fragen-, Antwort- und Routingprüfung im lokalen Daily-Container; akzeptierte Wahrheit bleibt beim fachlichen Owner
- `skill-reference` — skilllokale Kalibrierung, Pattern Memory und technische Referenz ohne allgemeine Normautorität
- `knowledge-topic`, `knowledge-source`, `knowledge-article`, `knowledge-inventory-item`, `knowledge-dataset`, `knowledge-assessment` und `knowledge-log` — geschlossene Knowledge-Klassen mit gemeinsamem Topic-/Provenance-Modul
- [[system/contracts/knowledge/topic-wiki-boundary]] — Topic-Owner, Source-/Article-Grenze, Lifecycle und abgeleitete Registry
- `finance-account`, `finance-payment-source-registry`, `finance-expense`, `finance-client-cost`, `finance-time-entry`, `finance-invoice`, `finance-recurring-obligation`, `finance-tax-dossier` und `finance-tax-manifest` — die durch den realen Finance-Bestand belegten Klassen
- [[system/contracts/finance/finance-system-boundary]] — externe Authority, State Machines, Sicherheits- und Ownergrenzen der Finance-Domain
- [[system/contracts/normative-system-architecture]] — semantischer Owner der Systemkategorien und Autoritätsgrenzen
- [[system/contracts/core/capability-interface]] — maschinenlesbarer I/O-, Template-, Invocation- und Check-Vertrag
- [[system/frameworks/core/verification-ownership]] — eindeutige Ownership aller Verification Assertions
- [[system/checks/pos-v1-contract]] — deklarativer Owner des ausführbaren Registry-Checks

## Maintenance

Änderungen an Registry, Foundation, Governance, Page Shapes, Modulen oder Profilen werden atomar mit Templates, Runtime, Fixtures, Generated Views und Changelog ausgeführt. Der Index wird nur angepasst, wenn ein Navigationseinstieg entsteht, verschoben, ersetzt oder retired wird; konkrete Change-Regeln bleiben bei `governance.yaml` und den verlinkten Systemverträgen.
