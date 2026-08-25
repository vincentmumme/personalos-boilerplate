---
schema_version: pos-v1
id: 01a00149-b5ad-7532-8064-ecfaf3f9c4b2
type: contract
title: "Daily Briefing Ownership and Delivery"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Daily Briefing Ownership and Delivery

## Contract

Ein Daily Briefing ist eine abgeleitete Entscheidungsvorlage im Daily-Container. Der Automation-Record besitzt Trigger und gewünschten Betrieb, der Skill besitzt Auswahl und Formulierung, der Daily-Record besitzt das persistierte Briefing und der Delivery-Kanal erhält ausschließlich dessen freigegebenen Nutztext.

## Scope

Der Vertrag gilt für Morning-, Midday-, Evening- und Ad-hoc-Briefings, unabhängig von Agent, Runtime, Host und Delivery-Kanal. Historische Morning-Briefing-Outputs unter `automations/` bleiben lesbare Evidenz, sind aber kein aktiver Zielpfad.

## Invariants

- Das Briefing priorisiert vorhandene Wahrheit und Live-Kontext; es erzeugt keine zweite fachliche Current Truth.
- Der persistierte Record liegt unter dem lokalen Daily-Tag und trägt die tatsächlich maßgebliche IANA-Zeitzone sowie einen RFC-3339-Erstellungszeitpunkt mit Offset.
- Host-Zeitzone und Scheduler-Zeitzone dürfen {{user_name}}s lokale Tageszuordnung nicht still bestimmen.
- Source Notes und Verification werden nicht an den Nutzerkanal ausgeliefert.
- Ein Delivery-Side-Effect erzeugt keine zweite Markdown-Kopie und kein eigenes Run-Receipt für einen gewöhnlichen erfolgreichen Lauf.
- Fehlende oder alte Quellen werden benannt; sie werden weder als Nullwert noch als aktuelle Wahrheit ausgegeben.

## Interfaces

- [[system/frameworks/daily/modularer-daily-kontext]] besitzt den Tagescontainer.
- [[system/rules/core/timezone-and-local-day-boundary]] löst Tag, Zeitzone und historische Stabilität auf.
- [[system/templates/daily/daily-briefing]] besitzt die persistierte Shape.
- Der Automation-Owner referenziert Capability, Runtime und Schedule; Observability misst den Laufzustand separat.
- Der owning Skill darf Sources read-only konsumieren und liefert nur den Inhalt aus `## Briefing` an den vorgesehenen Kanal.

## Compliance

Jeder Writer validiert Profile, Parent-Day, Zeitzone, erforderliche Abschnitte, Nutztextgrenzen und verbotene Payloads. Der aktive Prompt und alle Views dürfen keinen neuen `automations/<slug>/outputs/`-Pfad für Briefings vorschreiben.

## Evolution

Neue Briefing-Arten erweitern den kontrollierten Enum und verwenden dasselbe Daily-Profil. Ein neuer Delivery-Kanal ändert nicht den POS-Owner. Historische Automation-Outputs werden nur über eine eigene manifestierte Bestandswelle migriert oder archiviert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
