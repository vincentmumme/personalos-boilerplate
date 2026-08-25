---
schema_version: pos-v1
id: 019ffb7e-ecb3-73a4-b483-1a99e32af6d2
type: contract
title: "Business Object Model"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Business Object Model

## Contract

`business/` besitzt {{user_name}}s fortlaufende persönliche Business Truth in acht standardisierten Objektklassen:

| Objektklasse | Pfad | Primary Profile |
|---|---|---|
| Brands | `business/brands/` | `brand` |
| Markets | `business/markets/` | `market` |
| Customer Profiles | `business/customer-profiles/` | `customer-profile` |
| Products | `business/products/` | `product` |
| Offers | `business/offers/` | `offer` |
| Business Models | `business/business-models/` | `business-model` |
| Strategies | `business/strategies/` | `strategy` |
| Operating Models | `business/operating-models/` | `operating-model` |

Jedes Objekt beginnt als stabiler lesbarer Hauptrecord. Alle Profile teilen einen gemeinsamen State-Record-Rahmen und ergänzen ihre objektspezifischen Body Sections.

Zwei enge Brand-Companion-Typen sind zugelassen:

- `business/brands/<brand-slug>/tone-of-voice.md` mit Profile `brand-voice`
- `business/brands/<brand-slug>/design-system.md` mit Profile `brand-design-system`

Sie gehören genau einem vorhandenen Brand-Hauptrecord, besitzen eine eigene Current Truth und dürfen keine weiteren freien Child-Dateien legitimieren. Physische Design-Assets bleiben außerhalb des Markdown-Vaults.

## Scope

Der Vertrag gilt für wiederkehrende Business-Objekte, ihre Current Truth, Lifecycle, Relations, Sources und Timeline. Er gilt nicht für Company-Stammdaten, Project Working Truth, Deals, Tasks, Content-Produktion, Finance-Transaktionen, Interaction Evidence oder gemeinsam verbindliche BOS-Wahrheit.

## Invariants

1. Jede Business-Wahrheit besitzt genau einen Objektowner und darf nicht zusätzlich im Company- oder Brand-Record kopiert werden.
2. Company-, Brand- und Market-Zusammenhänge werden über typisierte Relations und abgeleitete Views verbunden.
3. Ein Hauptrecord bleibt unabhängig von seiner Komplexität stabil und lesbar benannt; UUIDv7 ist seine technische Identität.
4. Ein gleichnamiger Companion Directory darf nur entstehen, wenn ein zugelassener Companion-Artefakttyp und realer Inhaltsbedarf existieren.
5. Neue Child-Dateien oder freie Unterordner sind ohne Profile-Admission unzulässig.
6. Projects erarbeiten neue oder geänderte Business-Wahrheit. Erst angenommene Ergebnisse werden in den Business-Owner propagiert.
7. Ein Business Object mit externer kanonischer Wahrheit verwendet `authority_scope: pointer` und kopiert keine fremde Current Truth.
8. Der Acht-Klassen-Katalog ist geschlossen, aber durch ein vollständiges Admission-Paket erweiterbar.

## Interfaces

- `companies/` besitzt Legal Entity Truth und erzeugt über Relations beziehungsweise Indizes eine Company-Sicht.
- `projects/` besitzt Erstellung, Änderung, Research, Entwürfe und Cutover-Arbeit.
- `content/` konsumiert Brand-, Customer-, Offer- und Strategy-Wahrheit, besitzt aber die Content-Produktion.
- `finance/` besitzt Transaktionen, Konten, Rechnungen, Steuerprozesse und finanzielle Evidenz.
- Das `business-context`-Modul stellt optionale `company_refs`, `brand_refs` und `market_refs` bereit.

## Compliance

Registry, Profiles, Templates, positive und negative Fixtures sowie JSON Schemas prüfen den strukturellen Vertrag. Domain-Cutover benötigen zusätzlich ein vollständiges Legacy-Inventar, stabile UUID-Zuweisung, Link- und Consumerplan, Relation-Postflight sowie einen Recovery-Beleg.

## Evolution

Eine neue Objektklasse wird nur zugelassen, wenn mehrere reale Instanzen dieselbe dauerhafte Business-Semantik besitzen und keine der acht bestehenden Klassen passt. Companion-Artefakttypen werden bedarfsgetrieben separat zugelassen; der Hauptrecord selbst legitimiert keinen freien Dateibaum.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
