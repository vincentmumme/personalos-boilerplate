---
schema_version: pos-v1
id: 01a00204-a310-77ac-92ab-d58e9ddcc171
type: contract
title: "Historical Interaction Compatibility"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Historical Interaction Compatibility

## Contract

Historische Interaction-Artefakte dürfen in ihrer ursprünglichen, quellenbelegten Form verbleiben, wenn ihr Writer abgeschaltet ist, ihr Inhalt ausschließlich Evidence, Analyse oder technische Verarbeitungshistorie darstellt und keine fachliche Current Truth besitzt. Der alte Envelope ist dann bewahrte Quellenform, keine aktive Systemnorm.

Neue Signals, Calls und Conversations verwenden ausschließlich die registrierten `pos-v1`-Profile für Interaction Event, Conversation Stream, Source Evidence, Interaction Analysis und Processing Receipt. Ein alter Record darf weder als Template kopiert noch von einem aktuellen Writer fortgeschrieben werden.

## Scope

Der Vertrag umfasst historische monatliche Nachrichtenarchive, Audio-Transkripte, Call-Transkripte, Call-Summaries, Research-/Analysis-Artefakte, globale und streamlokale Runreports, alte Scanlogs sowie eindeutig abgegrenzte Notizen, Source Manifests und Media Reviews unter `/interactions`.

Aktive Conversation-Owner, neue Source Evidence, neue Interaction Analyses, technischer JSON-State und fachliche Domainowner fallen nicht unter die Legacy-Ausnahme.

## Invariants

1. Historische Evidence besitzt keine fachliche Current Truth und überschreibt keinen kanonischen Owner.
2. Jeder aktuelle Writer muss vor Freigabe nachweisen, dass er die Legacy-Pfade nicht mehr erweitert.
3. Bestehende Pfade und Inhalte bleiben unverändert, solange aktive Consumer darauf verweisen.
4. Löschen, Verschieben oder Umschreiben braucht ein vollständiges Pfad-/Hash-/Consumer-Manifest, Recovery und Postflight.
5. Eine alte `schema_version` allein ist weder Lösch- noch Migrationsgrund.
6. Technischer State ist maschinenlesbar; historische Markdown-Scanlogs und Pending-Views werden nicht als aktueller State fortgeschrieben.
7. Neue fachliche Erkenntnisse aus historischer Evidence werden explizit zum kanonischen Owner propagiert und nicht im Altartefakt aktualisiert.

## Interfaces

- [[system/frameworks/interactions/signal-evidence-und-processing]] definiert das aktuelle Zielmodell.
- [[system/contracts/core/source-provenance]] bindet Claims an Quellen.
- [[system/contracts/core/personalos-mutation-contract]] bindet jede spätere Bestandsmutation.
- historical interaction inventory hält das reproduzierbare Klasseninventar.

## Compliance

Der ausführbare Interaction-/Automation-Audit prüft die aktiven Writer getrennt vom historischen Bestand. Das historische Inventar zählt jede nicht zugelassene Interaction-Datei genau einmal, bindet seine Aggregate an einen Inventarhash und weist Sonderfälle einzeln aus. Ein neuer Writer-Test muss für seinen Zielpfad beweisen, dass keine Monatsarchive, Runreports, Scanlogs oder standalone Legacy-Transkripte entstehen.

## Evolution

Eine spätere physische Normalisierung darf klassenweise erfolgen, wenn sie einen konkreten Such-, Integritäts- oder Consumer-Nutzen besitzt. Ohne solchen Nutzen ist `retain-in-place` der terminale, regelkonforme Zustand. Der Vertrag wird erst retired, wenn kein Legacy-Interaction-Artefakt mehr existiert oder alle verbleibenden Klassen durch einen engeren Vertrag ersetzt sind.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
