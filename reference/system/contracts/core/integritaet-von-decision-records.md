---
schema_version: pos-v1
id: 019ff118-a31d-7d2d-b387-2bbab272df31
type: contract
title: "Integrität von Decision Records"
created: 2026-08-11
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.1
---

# Integrität von Decision Records

## Contract

Bestätigte Decision Records sind semantisch unveränderliche Provenance-Belege. Eine spätere Richtungsänderung wird durch einen neuen Record mit expliziter Supersession oder Reversal abgebildet und niemals durch rückwirkliches Umschreiben der ursprünglichen Wahl.

## Scope

Der Vertrag gilt für alle persönlichen, fachlichen, projectbezogenen, domainübergreifenden und systemischen Decision Records im PersonalOS unter dem kanonischen Root `/decisions/` sowie für unveränderliche historische Migrationsbelege.

## Invariants

- Ein Decision Record entsteht erst nach einer bestätigten Wahl; offene Fragen bleiben Working Truth oder Decision Gate.
- Entscheidung, damalige Begründung, Kontext und echte Alternativen werden nicht semantisch umgeschrieben.
- Tippfehler, kaputte Links, fehlende Quellen und eindeutig falsche Metadaten dürfen kontrolliert korrigiert werden.
- Materielle Korrekturen werden datiert und nachvollziehbar dokumentiert.
- Neue Richtung bedeutet neuer Record plus `supersedes` oder `reverses`; der alte Record bleibt erhalten und verlinkt den Nachfolger.
- Der Decision Record besitzt das Warum; der fachliche Owner besitzt die daraus geltende Current Truth.
- Folge-Actions, Owner-Updates, Backlinks und relevante Timeline-Ereignisse werden als eine Propagationsmenge behandelt.

## Interfaces

- [[decisions/index]] ist der kanonische Einstieg in den abgeschlossenen Decision-Root.
- [[system/frameworks/core/context-routing-and-truth-propagation]] bestimmt betroffene Owner und Reifegrad.
- [[system/contracts/core/personalos-mutation-contract]] bindet Korrektur, Supersession und Propagation.
- Das registrierte Decision Profile und [[system/templates/decision]] operationalisieren diesen Vertrag, dürfen ihn aber nicht verändern.

## Compliance

Nicht compliant sind rückwirkliche Bedeutungsänderungen, still entfernte Alternativen oder Gründe, fehlende Nachfolgerlinks, lokale Decision-Kopien sowie resultierende Current Truth, die nur im Decision Record und nicht beim fachlichen Owner existiert.

## Evolution

Neue Decision-Zustände, Relations oder Korrekturtypen werden über das Data-Model-Admission-Verfahren ergänzt. Eine Lockerung semantischer Unveränderlichkeit benötigt eine neue ausdrückliche Entscheidung und einen Migrationsplan für bestehende Decision-Ketten.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
