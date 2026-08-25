---
schema_version: pos-v1
id: 019ff118-a379-7a65-9df7-632ba72b65cb
type: framework
title: "Modularer Daily-Kontext"
created: 2026-08-11
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Modularer Daily-Kontext

## Purpose

Dieses Framework erzeugt einen agenten- und runtimeunabhängigen zeitlichen Querschnitt durch das PersonalOS, ohne Activity, Journal, Automation Runs und fachliche Current Truth in einer monolithischen Tagesdatei zu vermischen.

## Model

```text
Beliebige Producer
  -> atomare Activity Contributions
  -> optional persönliche Journal Entries
  -> Assembler verdichtet relevante Beiträge
  -> kompakter Day Record verlinkt Owner und Evidenz
```

Verbindliche Containerform:

```text
daily/<year>/<date>/
  <date>.md
  activity/<uuid>.md
  journal/<uuid>.md
  briefing/<uuid>.md
  context-gaps/<uuid>.md
  optionale zugelassene Tagesmodule
```

Der lesbare Day Record verwendet das Tagesdatum als Dateiname. Wiederholbare Activity Contributions und Journal Entries verwenden ihre stabile UUIDv7 als Dateiname. `day_date` und Pfad müssen übereinstimmen; genaue Zeitpunkte werden als RFC-3339-Timestamps mit Sekunden und Offset gespeichert.

## Components

- **Day Record:** kompakte Tagesübersicht und Navigation, keine zweite Domain Truth.
- **Activity Contribution:** atomarer, deduplizierbarer Beitrag eines Menschen, Agenten, Runtimes, Prozesses oder externen Signals.
- **Journal Entry:** optionale subjektive zeitgebundene Evidenz; nicht automatisch Current Truth.
- **Daily Briefing:** optionale abgeleitete Entscheidungsvorlage; priorisiert vorhandene Wahrheit und Live-Kontext, besitzt aber keine zweite Domain- oder Automation-Wahrheit.
- **Context Gap Review:** optionale abgeleitete Prüfung fehlenden oder unsicheren Kontexts; Fragen und Antworten werden zu kanonischen Ownern geroutet und bleiben keine zweite Wahrheit.
- **Producer Identity:** generische Actor-, Agent-, Runtime- und Process-Beziehungen statt hardcodierter Codex-/Runtime-Agent-Typen.
- **Assembler:** verdichtet Beiträge, aggregiert No-ops und erhält materielle Provenance.
- **Access Boundary:** vollständige POS-Agenten dürfen Activity und Journal standardmäßig laden; eingeschränkte Agenten werden am Runtime-/POS-Zugriff begrenzt.

## Decision Logic

1. Relevante Arbeit erzeugt einen Contribution Record oder eine äquivalente atomare Contribution; reine technische Zwischenschritte und wiederholte No-ops werden ausgelassen oder aggregiert.
2. Fachliche Ergebnisse werden zuerst zu ihren Ownern propagiert; Daily referenziert sie.
3. Journal, Briefings und Context Gap Reviews entstehen optional und dürfen mehrere Records pro Tag besitzen.
4. Ein Day Record wird aus Contributions, Journal und abgeleiteten Tagesmodulen verdichtet, ohne vollständige Runs, Transkripte oder Current Truth zu kopieren.
5. Ohne Activity oder Journal entsteht kein leerer Tagescontainer.
6. `/log` kann Contribution- oder Journal-Producer sein, ist aber kein notwendiges Abschluss-Gate.

## Interfaces

- Automation Runs verbleiben unter `automations/`; Interaction Evidence unter `interactions/`; Domain- und Project Truth bei ihren Ownern.
- [[system/frameworks/core/context-routing-and-truth-propagation]] steuert Owner-Propagation vor der Daily-Verdichtung.
- Day-, Contribution- und Journal-Profile sind über die Data-Model-Governance zugelassen und werden generisch durch die Registry validiert.
- Historische flache Daily Logs sind verlustfrei als Legacy-Ledger innerhalb ihres Day Records erhalten; sie wurden nicht mechanisch in hunderte scheinbar neue atomare Contributions zerlegt.
- Neue Writes verwenden ausschließlich die atomaren Zielprofile und die Systemtemplates unter `system/templates/daily/`.
- [[system/contracts/daily/briefing-ownership-and-delivery]] trennt Daily-Artefakt, Automation-Trigger, Skill-Verhalten und externen Delivery-Side-Effect.
- [[system/rules/core/timezone-and-local-day-boundary]] bestimmt lokale Tageszuordnung unabhängig vom ausführenden Host.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
