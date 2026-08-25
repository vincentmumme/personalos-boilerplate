---
schema_version: pos-v1
id: 019ff118-a254-7b64-ab46-3e7b013e6885
type: framework
title: "Action- und Attention-Modell"
created: 2026-08-11
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Action- und Attention-Modell

## Purpose

Dieses Framework klassifiziert handlungsrelevanten Kontext, damit Agents klare Commitments automatisch operationalisieren können, ohne Operations mit Ideen, Terminen, Wiedervorlagen oder fremden Aufgaben zu vermüllen.

## Model

```text
Signal oder Kontext
  -> eindeutiges persönliches Commitment?
     -> ja: Action
     -> bestehendes Commitment, externer nächster Schritt: Waiting
     -> noch keine Handlung, spätere Neubewertung nötig: Attention Trigger
     -> möglicherweise relevant, aber unklar: Candidate
     -> keine Verpflichtung: Idea, Capture, Project Candidate oder No-op
```

Die kanonische Action ist ein atomarer Record. Agentenansichten, Briefings und Todo-Listen sind abgeleitete Projektionen.

Section-Indizes unter `operations/actions/` und `operations/attention-triggers/` halten ausschließlich stabile Navigation und Ownergrenzen. Sie enumerieren keine Einzelrecords und besitzen keinen Live-Status; Agenten erzeugen jede aktuelle Sicht direkt aus den atomaren Records.

## Components

- **Action:** stabiles gewünschtes Ergebnis, Done-Grenze und genau ein aktueller nächster Schritt.
- **Lifecycle:** `ready`, `in-progress`, `waiting`, `blocked`, `deferred`, `completed`, `cancelled`.
- **Attention Trigger:** Zeitpunkt oder Ereignis für kontextuelle Neubewertung ohne vorweggenommene Action.
- **Candidate:** kurzlebiger Prüfzustand außerhalb normaler Action-Abfragen.
- **Timing:** `due`, `target`, `not_before`, `follow_up_at` und `review_at` besitzen getrennte Semantik.
- **Execution Boundary:** Agent führt sicher aus, bereitet bis zur Freigabe vor oder legt {{user_name}} nur den nicht delegierbaren Schritt vor.
- **Relationsgrenze:** `evidence_refs` verweist ausschließlich auf Quellen und Belege; `affected_owner_refs` verknüpft optional die Personen, Companies, Projects oder Domainowner, deren Wahrheit von der Action betroffen ist.

## Decision Logic

1. Vollständige Source lesen, bestehende Actions und Projects suchen und Dubletten ausschließen.
2. Nur ein eindeutiges Commitment mit persönlichem Owner zur Action machen; eindeutige externe Verpflichtung genügt als Evidenz.
3. Mehrdeutige Ableitungen als Candidate stagen und in einem begrenzten Triage-Zyklus zu Action, Trigger, Idea, Merge, Discard oder Ask disponieren.
4. Ein Attention Trigger liest bei Fälligkeit erneut den aktuellen Owner-Kontext: erledigt oder obsolet schließen, klare Action erzeugen, Mehrdeutigkeit fragen oder einen neuen Trigger setzen.
5. Lifecycle darf bei eindeutiger Evidenz automatisch wechseln; Alter, Schweigen oder vermutete Unwichtigkeit reichen niemals für Abschluss oder Löschung.
6. Vor terminalem Abschluss Ergebnis und Evidenz zu den betroffenen Ownern propagieren.

## Interfaces

- [[system/frameworks/core/context-routing-and-truth-propagation]] bestimmt Source, Reifegrad und Owner.
- [[system/contracts/core/personalos-mutation-contract]] bindet jeden daraus folgenden Write.
- Action-, Attention- und mögliche Candidate-Profile werden erst über das Data-Model-Admission-Verfahren aktiviert.
- Projects und Domains verlinken Actions, besitzen aber keine Schatten-Tasklisten.
- Shared Truth Systems bleiben Owner gemeinsamer Aufgaben; PersonalOS hält {{user_name}}s Action oder einen Pointer.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
