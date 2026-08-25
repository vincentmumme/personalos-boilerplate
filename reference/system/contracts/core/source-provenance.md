---
schema_version: pos-v1
id: 019ffc1a-c4f9-7cc9-b347-1c65547ce46b
type: contract
title: "Source Provenance"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Source Provenance

## Contract

Source Evidence, Analyse, Processing-Beleg und kompilierte Current Truth bleiben getrennte Schichten. Jede materielle Wahrheitsaussage muss zu der Evidenz, dem Ereignis, der Entscheidung oder der nachvollziehbaren Ableitung zurückverfolgbar sein, die sie trägt.

Dieser Vertrag ist der allgemeine Einstieg für jeden Weg von einem internen oder externen Signal zu einer Antwort, Handlung oder neuen PersonalOS-Wahrheit. Das ausführliche Verarbeitungsmodell liegt in [[system/frameworks/interactions/signal-evidence-und-processing]], die Ownerwahl in [[system/frameworks/core/context-routing-and-truth-propagation]] und der Schreibvorgang in [[system/contracts/core/personalos-mutation-contract]].

## Scope

Der Vertrag gilt für externe Signale, Calls, Nachrichten, Research, Dokumente, Datensätze, Automation-Runs, manuelle Eingaben, Entscheidungen und alle daraus propagierten Domain-Updates.

## Invariants

- Input ist Evidenz oder Kandidat, nicht automatisch Wahrheit.
- Source Evidence wird nicht still in eine fachliche Current Truth umetikettiert.
- Analyse benennt Ableitung, Unsicherheit, Widerspruch und Propagation, besitzt aber keine fachliche Wahrheit.
- Current Truth zitiert die kleinste hinreichende auflösbare Quelle oder Decision Evidence.
- Quellen stehen standardmäßig direkt hinter der von ihnen getragenen Aussage oder im unmittelbar zugehörigen Absatz. Eine getrennte Sources-Sektion ergänzt die Übersicht, ersetzt aber nicht die Zuordnung einzelner materieller Claims.
- Timeline-Einträge benennen Datum, Änderung und Evidenz; sie sind keine zweite Current Truth.
- Schwächere neue Evidenz überschreibt keine stärkere belegte Wahrheit ohne sichtbare Konfliktauflösung.
- Ein Quellenlink muss auflösbar, providerunabhängig verständlich oder durch einen sicheren externen Pointer dokumentiert sein.
- Secret- oder sensible Rohwerte werden nicht nur für Provenance dupliziert.
- Eine Agentenantwort trennt belegte Aussage, berichtete Aussage, Ableitung, Unsicherheit und Empfehlung. Fehlt eine hinreichende Quelle oder widersprechen sich Quellen, wird dies ausdrücklich gesagt statt Sicherheit zu simulieren.

## Interfaces

[[system/frameworks/interactions/signal-evidence-und-processing]] definiert die Processing-Schichten. [[system/frameworks/core/context-routing-and-truth-propagation]] bestimmt Zielowner und Propagation. [[system/conventions/core/claim-nahe-quellenplatzierung]] bestimmt die lesbare Platzierung von Quellen im Body. Source-, Interaction-, Decision- und Domainprofile typisieren die jeweiligen Relations; Templates dürfen keine untypisierte generische `sources`-Ablage erfinden.

## Compliance

Ein Writer muss vor dem Commit Quelltyp, Owner, Relation und Propagation bestimmen. Bei unvollständiger Evidenz bleibt der Zustand offen, unsicher oder als Capture gestaged. Verifier prüfen Linkauflösung, zulässige Zielprofile und das Vorhandensein der profilgebundenen Source-/Timeline-Sektionen.

## Evolution

Neue Source-Arten benötigen nur dann ein eigenes Profil, wenn Lifecycle, Retention oder Relations materiell verschieden sind. Provider- oder Kanalnamen allein legitimieren kein neues allgemeines Provenance-Modell.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
