---
schema_version: pos-v1
id: 01a0015e-8a7b-71c7-8085-26ea01339db2
type: contract
title: "Context Gap Review Ownership and Propagation"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Context Gap Review Ownership and Propagation

## Contract

Ein Context Gap Review ist eine abgeleitete Tagesprüfung, welche fehlender, unsicherer oder widersprüchlicher Kontext die künftige Unterstützung {{user_name}}s konkret verbessert. Der Review besitzt Fragen, Antworten, Routingentscheidungen und Verifikation; akzeptierte Wahrheit bleibt ausschließlich beim fachlichen Owner.

## Scope

Der Vertrag gilt für Question Batches, Answer Ingest, Feedback Reviews und gelegentliche Deep Maps. Er gilt unabhängig davon, welcher Agent oder welche Runtime den Review erzeugt. Historische Context-Gap-Automation-Outputs bleiben Herkunftsevidenz und werden nicht pauschal rückmigriert.

## Invariants

- Ein Review erzeugt keine zweite Identity-, People-, Company-, Business-, Project-, Finance-, Health- oder Operations-Wahrheit.
- Ein `question-batch` enthält standardmäßig genau fünf priorisierte, beantwortbare Fragen mit erkennbarem Owner und Nutzen.
- Eine Antwort wird als Current Truth nur durch einen belegten Write beim kanonischen Owner akzeptiert; der Review hält danach ausschließlich Quelle und Propagation fest.
- Tasks, Waiting States und Wiedervorlagen werden über den Operations-Owner geroutet und nicht im Review verwaltet.
- Kalibrierung des Fragemusters darf skilllokal liegen; private Antworten und fachliche Wahrheit dürfen dort nicht landen.
- Lokaler Tag, Zeitzone und Erstellungszeitpunkt folgen der gemeinsamen Zeitzonenregel und bleiben historisch stabil.

## Interfaces

- [[system/frameworks/daily/modularer-daily-kontext]] besitzt den Tagescontainer.
- [[system/templates/daily/context-gap-review]] besitzt die persistierte Shape.
- [[system/frameworks/core/context-routing-and-truth-propagation]] besitzt die Owner-Propagation.
- [[system/contracts/core/personalos-mutation-contract]] besitzt die Mutations- und Approval-Grenze.
- Der owning Skill besitzt Kandidatenauswahl, Fragelogik und skilllokale Kalibrierung.

## Compliance

Jeder Write validiert Profil, Parent Day, IANA-Zeitzone, Offsetzeit, Sections, Routing und Provenance. Ein Question Batch prüft zusätzlich die exakte Zahl priorisierter Fragen. Allgemeine Regeln aus der Kalibrierung werden unter `/system` propagiert statt als konkurrierende Skillnorm weitergeführt.

## Evolution

Neue Review-Arten erweitern den kontrollierten Enum. Eine wiederkehrende Automation benötigt vor Aktivierung einen eigenen Automation Record, explizite Schedule-Zeitzone und Observability; das Daily-Profil selbst begründet keinen Scheduler.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
