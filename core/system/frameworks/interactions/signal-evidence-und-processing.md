---
schema_version: pos-v1
id: 019ff59c-3071-7ecf-994d-3769e76dd364
type: framework
title: "Signal Evidence und Processing"
created: 2026-08-12
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Signal Evidence und Processing

## Purpose

Dieses Framework trennt für alle heutigen und zukünftigen Signalquellen eindeutig Kommunikationsereignis oder nicht-menschlichen Signal Digest, Source Evidence, Analyse, fachliche Propagation und Automation-Verarbeitung. Es verhindert zweite Wahrheit und bleibt unabhängig von WhatsApp, Gmail, Discord, Calls, News-, Web- oder Creator-Quellen sowie einem bestimmten Agenten und Runtime-Setup.

## Model

```text
externes Signal oder Gespräch
  -> Interaction Event, Conversation Stream oder Signal Digest
  -> redigierte Source Evidence
  -> Interaction Analysis
  -> fachliche Wahrheit beim genau einen Owner
  -> Action / Attention / Decision nur bei erfüllter Schwelle
  -> Automation Receipt bei materiellem Run
  -> Automation Day Summary für vollständige Tages-Coverage
```

## Components

- **Interaction Event:** einmaliges Gespräch, Call, Workshop oder Treffen. Der Hauptrecord ist die Tür in das Ereignispaket.
- **Conversation Stream:** fortlaufender Kommunikationskanal. Er besitzt nur Current Truth über Beteiligte, Kanal, Coverage, letzte materielle Kommunikationsentwicklung und Quellenlücken.
- **Signal Digest:** datierte quellengebundene Verdichtung nicht-menschlicher News-, Web-, Creator- oder Monitoring-Signale. Er besitzt keine automatisch angenommene Knowledge-, Content- oder Domainwahrheit.
- **Source Evidence:** Transcript, redigierte Nachrichtencharge, Source Card, Asset-Pointer oder interaction-spezifische Research-Evidenz. Sie belegt, ohne fachliche Current Truth zu besitzen.
- **Interaction Analysis:** nicht-kanonische Interpretation der Evidenz mit Widersprüchen, Unsicherheit, Propagation und No-op-Entscheidungen.
- **Fachlicher Owner:** People-, Company-, Project-, Operations-, Knowledge-, Finance-, Health-, Content- oder anderer Domainrecord, der die resultierende Current Truth besitzt.
- **Automation Run Receipt:** unveränderlicher Einzelbeleg eines materiellen, fehlerhaften, offenen, extern mutierenden oder auditpflichtigen Runs.
- **Automation Day Summary:** kompakter Tagescontainer mit Coverage, Freshness, Run-Zählung und Links zu materiellen Receipts.
- **Automation Record:** kanonische Current Truth über die Automation als stabiles Systemobjekt; verlinkt Zweck, Lifecycle, Trigger, Capability, Runtime, Inputs, Outputs, Credential-Anforderungen und Health, ohne diese Owner zu kopieren.
- **Technischer State:** maschinenlesbarer Cursor-, Dedupe-, Scheduler- und Recovery-Zustand. Er ist Runtime State und keine Markdown-Wahrheit.

## Decision Logic

1. Zuerst wird vollständig und redigiert erfasst, was die Quelle tatsächlich geliefert hat.
2. Ein Interaction Record beschreibt ausschließlich Kommunikation, Ereignis oder quellengebundene Signalverdichtung und verweist für fachliche Wahrheit auf deren Owner.
3. Die Analyse entscheidet pro plausiblem Owner `update`, `reference`, `no-op`, `stage` oder `ask` und hält Widersprüche sichtbar.
4. Der Automation Record ist der kanonische Einstieg in die Automation. Ausführbares Verhalten bleibt beim Skill, Runtime-Istzustand beim Systemowner und fachliche Wahrheit bei der Domain.
5. Ein Automation Receipt beschreibt den Verarbeitungslauf, nicht erneut die gesamte Source Evidence und nicht die daraus entstandene Current Truth.
6. Routine-No-op-Runs bleiben im technischen State und Tagesaggregat. Jede Ausnahme braucht einen konkreten Auditgrund.
7. Interaction Research bleibt im Paket, wenn es nur Claims des Ereignisses prüft. Wiederverwendbares Wissen wird zu `knowledge/` oder zum zuständigen Domainowner propagiert.
8. Binäre Medien liegen außerhalb der Markdown-Wahrheitsschicht; Records halten sichere Metadaten, Transkripte oder Asset-Pointer.
9. Ein technischer JSON Companion darf mechanische Detaildaten eines Digests halten, besitzt aber keine zweite Markdown-Wahrheit und darf den Digest nicht semantisch ersetzen.

## Interfaces

- [[system/frameworks/core/context-routing-and-truth-propagation]] bestimmt Owner und Propagation.
- [[system/rules/automations/material-run-receipt-retention]] bestimmt, wann ein Einzelbeleg entstehen darf und muss.
- [[system/contracts/core/personalos-mutation-contract]] bindet fachliche Writes.
- [[system/conventions/core/record-naming-and-temporal-paths]] bestimmt lesbare Eventpfade und UUID-Dateinamen atomarer Records.
- SKILL sowie source-spezifische Skills führen den Vertrag aus.
- Primary Profiles und Templates bestimmen die persistierten Record-Shapes.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
