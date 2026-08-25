---
schema_version: pos-v1
id: 019fffaf-279b-7724-89a2-b50812ade40e
type: contract
title: "Domain Ownership and Admission"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Domain Ownership and Admission

## Contract

Eine Domain ist ein dauerhafter fachlicher Wahrheitsraum für wiederkehrende Zustände, Beziehungen und Abläufe eines wesentlichen Lebens- oder Arbeitsbereichs. Sie besitzt eine eigene Root-Berechtigung nur dann, wenn diese Wahrheit weder sinnvoll als zeitlich begrenztes Project noch als Objekt eines bestehenden Owners geführt werden kann.

`content/`, `finance/`, `health/` und `knowledge/` sind zugelassene spezialisierte Domains. `business/`, `identity/`, `people/`, `companies/`, `operations/`, `interactions/`, `automations/` und `daily/` sind ebenfalls dauerhafte Owner, folgen wegen ihrer eigenen Systemrollen jedoch ihren spezifischen Verträgen. Dieser Vertrag ist das gemeinsame Meta-Framework für heutige und künftige fachliche Domains.

## Scope

Der Vertrag gilt für die Begründung eines Domain-Roots, seine minimale interne Architektur, neue Domain-Objektklassen, Domain-Profile und -Templates, den Übergang von Project Working Truth zu fachlicher Current Truth sowie die Anbindung externer Truth Systems, Sources, Automations und Assets.

## Invariants

1. **Dauer statt Vorhaben:** Eine Domain besitzt fortlaufende fachliche Current Truth. Ein Project besitzt zeitlich begrenzte Erarbeitung, Veränderung oder Migration. Arbeit an einer Domain findet im Project statt; akzeptierte Ergebnisse werden zum Domain-Owner propagiert.
2. **Genau ein Owner:** Jede fachliche Wahrheit hat genau einen kanonischen Owner. Andere Bereiche halten Relations, abgeleitete Views oder Pointer, aber keine zweite Current Truth.
3. **Root-Test:** Ein neuer Domain-Root ist nur zulässig, wenn ein realer, wiederkehrender Wahrheitsbestand mit mehreren Instanzen oder Lifecycles nachweislich in keinen bestehenden Owner passt. Umfang, Dateiformat, ein einzelnes Tool oder ein einzelnes Project reichen nicht aus.
4. **Ausdrückliche Freigabe:** Ein neuer Root benötigt immer {{user_name}}s ausdrückliche Entscheidung. Agenten dürfen einen Bedarf dokumentieren, aber keinen Root selbst legitimieren oder anlegen.
5. **Minimale Domainhülle:** Jede zugelassene Domain besitzt einen kanonischen `index.md`, einen Boundary Contract, klar benannte Objekt- und Lifecycle-Grenzen, Source-/Truth-/Action-Grenzen, Interfaces zu anderen Ownern und einen definierten Prüfweg.
6. **Keine vorsorglichen Module:** Unterordner, Profile, Companion Records und Templates entstehen erst bei realem wiederholtem Bedarf. Ein leerer Standardordner ist keine Architektur.
7. **Wiederholte Shapes werden registriert:** Wiederkehrende POS-Records benötigen vor breitem Write ein Primary Profile und ein Template unter `system/`. Einmalige fachliche Dokumente dürfen innerhalb des Domainvertrags entstehen, ohne vorsorglich einen universellen Typ zu erfinden.
8. **Source ist nicht Truth:** Eingehende Signale und Rohbelege bleiben als nachvollziehbare Evidenz bei ihrem Source-Owner. Die Domain hält nur die fachlich angenommene Wahrheit und ihre Source Relations.
9. **Action ist nicht State:** Aufgaben und Wiedervorlagen liegen unter `operations/`. Die Domain hält den fachlichen Zustand, aus dem Actions entstehen oder auf den sie wirken.
10. **Externe Authority bleibt extern:** Besitzt ein Fachsystem die kanonische Detailwahrheit, hält PersonalOS einen belegten Pointer, agentisch relevanten Kontext und zulässige Ableitungen. Es entsteht keine unmarkierte Parallelwahrheit.
11. **Assets folgen ihrem Owner:** Große oder binäre Assets liegen außerhalb des Markdown-Vaults. Die Domain hält Manifest, Metadaten, Provenance und Pointer gemäß [[system/contracts/core/file-and-asset-boundary]].
12. **Zeitpartitionierung ist eine Eigenschaft des Records:** Jahresordner werden nur für anwachsende, zeitbezogene Recordserien verwendet. Stabile Entitäten, Profile, Verträge und Current-Truth-Hauptrecords werden nicht künstlich nach Jahren partitioniert.

## Interfaces

Der minimale Domainfluss lautet:

```text
Source / Interaction / Automation
  -> belegte Analyse oder Normalisierung
    -> Domain Current Truth
      -> optionale Action in operations/

Project Working Truth
  -> ausdrückliche Annahme / Cutover
    -> Domain Current Truth
      -> Project hält nur Ergebnisbeleg und Relation
```

Für jede Domain werden folgende Rollen explizit benannt:

- **Truth Owner:** Welche Zustände und Beziehungen gehören ausschließlich hierher?
- **Source Owner:** Wo liegen Rohsignal, Transkript, Beleg oder Provider-Response?
- **Execution Owner:** Welcher Skill oder welche Automation darf den Zustand verändern?
- **External Authority:** Welches externe System bleibt gegebenenfalls kanonisch?
- **Project Boundary:** Welche Änderungen werden zuerst als Project erarbeitet?
- **Consumer Boundary:** Welche anderen Owner dürfen nur lesen, verlinken oder ableiten?

## Compliance

Eine neue oder wesentlich veränderte Domain wird erst aktiv, wenn mindestens Boundary Contract, Root Index, Objekt-/Lifecycle-Modell, Interfaces, Resolver-/Skill-Routing, benötigte Profile und Templates sowie ein write-spezifischer Check vorhanden sind. Bei Legacy-Bestand kommen vollständiges Inventar, Mapping, Consumer- und Linkplan, Dry Run, Recovery-Grenze und Postflight hinzu.

Ein Domain-Record ist nicht compliant, wenn sein Owner nur aus dem aktuellen Ordner abgeleitet wird, dieselbe Wahrheit parallel in Project, Company, Business oder Automation gepflegt wird, ein Providerformat ungeprüft zum Datenmodell wird oder ein leeres Universaltemplate fachliche Unterschiede verdeckt.

## Evolution

Neue Objektklassen werden zuerst als reale Instanzen oder Project Working Truth beobachtet. Erst wiederholte stabile Semantik rechtfertigt Profile, Templates oder neue Module. Ein bestehender Domain-Root kann nur durch eine neue ausdrückliche Decision und einen verlustfreien Owner-Cutover entfernt oder zusammengeführt werden.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
