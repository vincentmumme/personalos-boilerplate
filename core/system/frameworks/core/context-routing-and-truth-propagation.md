---
schema_version: pos-v1
id: 019fec8b-0c07-7ade-8360-70110c9d8b6f
type: framework
title: "Context Routing and Truth Propagation"
created: 2026-08-10
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Context Routing and Truth Propagation

## Purpose

Dieses Framework strukturiert, wie neue Informationen klassifiziert, einem kanonischen Owner zugeordnet und ohne zweite Wahrheit in alle materiell betroffenen Kontexte propagiert werden. Es ersetzt die allgemeine Routing-Semantik von `pos-operations`, nicht den Skill Resolver oder fachliche Domainentscheidungen.

## Model

```text
Input oder Signal
  -> Evidenz und Quelle bestimmen
  -> semantischen Delta-Typ bestimmen
  -> Reifegrad bestimmen
  -> kanonischen Owner bestimmen
  -> Propagation Map bilden
  -> spezifischen owning Skill ausführen
  -> über Mutation Contract schreiben und prüfen
```

Routing beantwortet nicht nur „In welchen Ordner?“, sondern getrennt:

1. Was wurde beobachtet, gesagt, empfangen oder entschieden?
2. Ist es Evidenz, Event, Working Truth, aktuelle State Truth, Action, Decision, Knowledge oder kein dauerhafter Delta?
3. Ist es lediglich erfasst, noch offen, vorgeschlagen, entschieden, umgesetzt oder bereits geltende Wahrheit?
4. Welcher Record beziehungsweise welches externe Truth System besitzt die aktuelle Wahrheit?
5. Welche angrenzenden Owner benötigen Update, Referenz, No-op, Staging oder Rückfrage?

## Components

- **Source/Evidence:** nachverfolgbare Grundlage des Signals; bleibt von daraus abgeleiteter Wahrheit unterscheidbar.
- **Delta:** die engste Aussage darüber, was sich gegenüber dem bestehenden Kontext wirklich geändert hat.
- **Semantic Class:** Event, State, Working Truth, Idea, Action, Decision, Knowledge, View, Run/Receipt oder transiente Information.
- **Maturity:** Erfassung, offene Prüfung, Vorschlag, Entscheidung, Umsetzung oder geltende Current Truth.
- **Canonical Owner:** genau ein Record oder autorisiertes externes Truth System für die aktuelle Aussage in ihrem Scope.
- **Propagation Map:** Liste plausibler Ziele mit `update`, `reference`, `no-op`, `stage` oder `ask`, Begründung und Source-Basis.
- **Owning Capability:** spezifischster Skill oder direkte Agentenhandlung, die fachliche Ausführung und zulässige Writes besitzt.

## Decision Logic

1. Der Resolver sucht zuerst den spezifischsten owning Skill. Ein allgemeiner POS-Router wird nicht vorgeschaltet.
2. Ein Signal bleibt Evidenz, bis eine ausreichend belegte neue Wahrheit oder ein bestätigter Handlungszustand erkannt ist.
3. Eine Idee oder sprachlich mögliche Aufgabe wird nicht ohne bestätigten Commit zur Action Truth. Eine bewusst bewahrte Idea liegt beim genau einen fachlichen Owner; Content-Ideen bleiben im ContentOS und eine mögliche spätere Initiative bleibt Domain-Idea, bis die Project-Schwelle erfüllt ist.
4. Working Truth verbleibt beim Project oder Arbeitsowner, bis ein fachlicher Cutover sie zur Current Truth des Zielowners macht.
5. Für jeden plausiblen Zielowner wird bewusst entschieden: `update`, `reference`, `no-op`, `stage` oder `ask`.
6. Dieselbe aktuelle Wahrheit wird nicht in mehrere Owner geschrieben. Nachbarflächen erhalten bei Bedarf Links, Provenance, Views oder Receipts.
7. Wenn Owner, Scope oder Reifegrad materiell unklar bleibt, wird kontrolliert gestaged oder {{user_name}} gefragt; es wird keine neue Struktur erfunden.

## Interfaces

- [[skills/RESOLVER]] routet Intent zu Capabilities und bleibt der einzige Skill Resolver.
- [[system/contracts/core/personalos-mutation-contract]] bindet jede resultierende POS-Mutation.
- [[system/contracts/core/system-artifact-ownership-and-capability-boundary]] bestimmt System- und Skillownership.
- Primary Profiles, Relations und Authority-Module bestimmen zulässige Record-Owner und externe Wahrheitsgrenzen.
- Owning Skills konsumieren dieses Framework über `system_refs`, wenn ihre Ausführung neue Wahrheit oder cross-domain Propagation erzeugen kann.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
