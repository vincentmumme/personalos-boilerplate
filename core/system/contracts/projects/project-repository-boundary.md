---
schema_version: pos-v1
id: 019ffc1a-c4f9-7528-8d85-aee0d5dd3262
type: contract
title: "Project and Repository Boundary"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Project and Repository Boundary

## Contract

Ein Project ist ein Vorhaben und besitzt seine Current Truth, Entscheidungen, Planung, Evidenz und Deliverables im zuständigen Truth System. Ein Repository ist ein technischer Implementierungs- und Versionsraum. Weder braucht jedes Project ein Repository noch ersetzt ein Repository den Project-Owner.

## Scope

Der Vertrag gilt für private, geschäftliche, Kunden-, Migrations-, Reise-, Content- und geteilte Projects sowie für lokale, synchronisierte oder externe Code- und Dokument-Repositories.

## Invariants

- Project- und Repository-Identität bleiben getrennt.
- Repo-Dateiinventare, Implementierungsdetails, Code, technische Specs und Build-Artefakte bleiben im Repository.
- Project Current Truth, Scope, Stakeholder, Phase, Entscheidungen, Risiken und fachliche Ergebnisse bleiben beim Project-Owner.
- Ein Project darf null, ein oder mehrere Repositories referenzieren.
- Repository-Referenzen verwenden stabile logische Identifier oder registrierte Pointer statt hostabhängiger absoluter Pfade.
- Geteilte oder externe Project Truth wird im PersonalOS als Authority-Pointer markiert und nicht unbemerkt kopiert.

## Interfaces

[[system/contracts/projects/universal-project-object]] bestimmt das Project-Modell. Repository-Relations werden nur über ein registriertes Project-Modul oder einen Companion-Record aufgenommen. Umsetzungsergebnisse werden als Evidence oder Deliverable verlinkt; ein Repo-Commit wird nicht automatisch zur Project-Entscheidung.

## Compliance

Beim Anlegen eines Projects wird kein Repository vorausgesetzt. Beim Verknüpfen eines Repositories werden Owner, logischer Identifier, Truth-Grenze und erwartete Rückpropagation dokumentiert. Absolute lokale Pfade dürfen nur in Runtime-Konfiguration oder auflösbaren Registries vorkommen.

## Evolution

Ein späteres Repository-Pointer-Profil kann Resolver, Hostpfade und Remote-URLs typisieren. Es muss die Trennung beibehalten und darf bestehende Project-Profile nicht in Repo-Metadaten aufblähen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
