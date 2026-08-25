---
schema_version: pos-v1
id: 019ffb77-265c-73e6-b497-40567abe7057
type: contract
title: "Identity Subject and Facets"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Identity Subject and Facets

## Contract

`identity/` besitzt die dauerhafte Wahrheit über den Menschen, dessen PersonalOS dies ist. Der Bereich besteht aus genau einem kanonischen Subject-Hauptrecord und einem geschlossenen, kontrolliert erweiterbaren Katalog standardisierter Facetten.

Der Hauptrecord ist immer `identity/<subject-slug>.md`. Die Standardfacetten sind:

- `identity/biography.md`
- `identity/personal-constitution.md`
- `identity/operating-profile.md`
- `identity/life-orientation.md`
- `identity/legal-identity.md`

`identity/capabilities.md` ist optional und wird erst materialisiert, wenn genügend dauerhafte, belegbare Inhalte vorliegen. `identity/index.md` navigiert Subject, materialisierte Facetten, angrenzende Owner und die Pflegegrenze.

## Scope

Der Vertrag gilt für menschliche Identity-Wahrheit, Root-`USER.md` als kompakte Projektion und alle zukünftigen Identity-Facetten. Er definiert weder `people/` noch Business-, Project-, Finance-, Health- oder Agentenwahrheit.

## Invariants

1. Der Mensch hinter dem PersonalOS besitzt genau einen `identity-record` und keinen parallelen vollständigen `people/`-Record.
2. Jede Facette verweist über `subject_ref` auf diesen Hauptrecord.
3. Der Hauptrecord aggregiert keine vollständigen Facetteninhalte, sondern hält Kernidentität, Navigation und angrenzenden Kontext.
4. Alle Facetten sind `state-records` mit `Current Truth`, Quellen und append-only Timeline.
5. Konkrete Veränderungsvorhaben bleiben Projects. Eine Facette darf nur deren dauerhaftes Ergebnis oder einen Pointer halten.
6. Business-, Company-, Finance- und Health-Wahrheit bleibt bei ihren kanonischen Ownern.
7. Legal Identity darf bewusst benötigte persönliche Identifikatoren halten. Secrets, Zugangsdaten, Karten- und Zahlungsdaten bleiben außerhalb des Markdown-Vaults im Secrets Manager.
8. Identity bleibt zunächst flach. Ein neuer Facettentyp oder Companion Directory benötigt ein vollständiges Admission-Paket und eine bestätigte semantische Lücke.
9. Leere optionale Facetten werden nicht prophylaktisch angelegt.
10. Boilerplate-Templates enthalten keine Personendaten; konkrete Instanzen dürfen den Subject-Kontext vollständig ausfüllen.

## Interfaces

- `USER.md` konsumiert den Hauptrecord als agentisch kuratierte Startprojektion.
- `SOUL.md` darf stabilen Arbeitskontext beschreiben, verweist für die vollständige persönliche Wahrheit aber auf Identity.
- `people/`, `companies/`, `business/`, `projects/`, `finance/` und `health/` verlinken den Subject-Hauptrecord oder die zuständige Facette, ohne deren Wahrheit zu kopieren.
- Profile, Templates und das `subject-context`-Modul unter `system/data-model/` bilden die maschinenlesbare Schnittstelle.

## Compliance

- Registry- und Fixture-Tests prüfen Profile, Pfade, Pflichtfelder und Body Shapes.
- Vollständige Relation-Auflösung prüft `subject_ref` und die Autorität des Hauptrecords.
- Ein Identity-Cutover benötigt ein verlustfreies Quellinventar, einen exakten Owner- und Linkplan sowie einen Recovery-Beleg.
- Reviews prüfen zusätzlich, ob Project-, Finance- oder Business-Wahrheit fälschlich in Identity dupliziert wurde.

## Evolution

Neue Facetten werden nur zugelassen, wenn vorhandene Facetten den Kontext semantisch nicht tragen können, wiederholbare Instanzen oder klarer Agentennutzen bestehen und Profile, Template, Fixtures, Migration Mapping sowie Validator gemeinsam aufgenommen werden. Temporäre Notizen erzeugen keinen neuen Facettentyp.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
