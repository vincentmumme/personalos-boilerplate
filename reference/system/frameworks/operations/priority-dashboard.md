---
schema_version: pos-v1
id: 01a0251c-9e0e-73a7-b499-da85e373e21d
type: framework
title: "Priority Dashboard"
created: 2026-08-21
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Priority Dashboard

## Purpose

Dieses Framework definiert eine kleine, morgentaugliche Prioritätssicht über bestehende Actions, Attention Trigger und ihre fachlichen Owner. Es schafft keinen zweiten Task-Speicher und besitzt weder Completion noch fachliche Lifecycle-Wahrheit.

## Model

```text
Actions + Attention Trigger + relevante Owner
                  +
        befristeter Priority Control
                  |
                  v
  operations/priority-dashboard.md
                  |
                  +-> {{user_name}}
                  +-> Morning Briefing
```

`operations/actions/` bleibt der einzige lokale Owner bestätigter Commitments. `operations/attention-triggers/` bleibt der Owner späterer Neubewertung. Projects, Domains, Deadlines, Evidenz und Lifecycle bleiben bei ihren bestehenden Ownern. Das Dashboard referenziert diese Records und erklärt die Auswahl, kopiert aber keinen unabhängigen State.

## Components

- Atomare Actions liefern Commitment, Lifecycle, Datum, Next Action und Done Boundary.
- Attention Trigger liefern ausschließlich fällige Neubewertung ohne vorweggenommene Action.
- Verlinkte Projects und Domainowner liefern Impact und aktuellen Kontext.
- Priority Control liefert befristete manuelle Richtung.
- Priority Dashboard ist die generierte, nicht-kanonische Projektion.

## Decision Logic

Die Auswahl folgt in dieser Reihenfolge:

1. noch wirksame, ausdrücklich von {{user_name}} gesetzte manuelle Richtung aus priority control;
2. echte `due`-Fälligkeiten und Zusagen im rollierenden Sieben-Tage-Fenster;
3. explizite `critical`-/`high`-Priorität und tatsächlich `in-progress` befindliche Arbeit;
4. Impact und aktueller Zustand verlinkter Projects oder fachlicher Owner;
5. `target` ausschließlich als weicher Planungs-Tie-Breaker;
6. Opportunities ohne aktuelle feste Zusage.

`target` ist keine Deadline und erzeugt weder allein Tagesfokus noch Überfällig-Dringlichkeit. Freitext wie `weekly`, `daily`, `monatlich` oder `wiederkehrend` ist kein Ranking-Signal. Ein wirklich wiederkehrendes Commitment wird durch seine aktuelle konkrete Action mit echter Fälligkeit oder Priorität beziehungsweise durch einen fälligen Attention Trigger sichtbar.

Manuelle Ausschlüsse entfernen einen Record nur aus der Sicht, nie aus seinem kanonischen Owner. Abgelaufene Controls werden automatisch ignoriert und im Dashboard sichtbar als abgelaufen markiert. Ein User-Override schlägt jede automatische Empfehlung, solange er wirksam ist.

## Bounded View

Die Sicht besitzt sechs getrennte Bereiche:

- genau ein aktueller Fokus;
- höchstens drei Outcomes im rollierenden Sieben-Tage-Fenster;
- zusätzliche 30-Tage-Lebens- und Reisegates, wobei aktueller Fokus, Sieben-Tage-Outcomes und Lebensgates zusammen höchstens fünf Actions enthalten;
- Kunden-, Cashflow- und Waiting-Risiken sowie fällige Neubewertung; innerhalb dieser Lane stehen Finance- und Delivery-Kontext vor persönlichem Waiting;
- gebündelte Finance-/Admin-Arbeit: gewöhnliche Eingangsbelege bleiben außerhalb der letzten fünf Kalendertage des Monats unsichtbares Sammelgut und erscheinen erst im Monatsendfenster als gemeinsamer Buchungs-Batch; nur echte Zahlungsfristen, Mahnungen, Cashflow-, Rechts- oder Leistungsrisiken dürfen vorher in andere Lanes eskalieren;
- Stale Review für alte, widersprüchliche oder realistisch neu zu planende Records.

Jeder Eintrag nennt seinen Prioritätsgrund. Alte überfällige Records ohne aktuelle Bestätigung werden nicht still als aktuellen Fokus behandelt, sondern sichtbar im `Stale Review` zur Neubewertung eingeordnet. Dadurch bleibt Drift sichtbar, ohne den Fokus mit alten Schleifen zu fluten.

## Manual Control

priority control besitzt ausschließlich temporäre Fokusfelder, Reihenfolge und Ausschlüsse als Links auf Actions. Der Record benötigt eine Review-Grenze; ein aktiver Control zusätzlich ein Ablaufdatum. Er darf keine Checkboxen, kopierten Next Actions, Done Boundaries, Completion oder unabhängige Task-Lifecycles enthalten.

Nach einer manuellen Änderung wird der deterministische Rebuild mit `--reason manual-priority-change` ausgeführt. Nach einer materiellen Action-, Trigger- oder Owner-Änderung ist `--reason operational-state-change` der explizite Refresh-Pfad. Es besteht kein Realtime-Watcher; zusätzlich läuft täglich ein geplanter Pre-Briefing-Rebuild. Consumer prüfen vor Nutzung mit `--check`, ob der gespeicherte Source-Digest noch dem aktuellen Action-/Trigger-/Control-/Project-Bestand entspricht; eine stale Sicht wird rebuilt oder sichtbar abgelehnt.

## Interfaces

- [[skills/task-manager/SKILL]] besitzt Action-, Trigger- und Lifecycle-Mutationen.
- [[skills/priority-dashboard/SKILL]] besitzt Ableitung, Control-Interpretation und Rebuild.
- SKILL konsumiert die fertige Sicht und rankt Actions nicht parallel neu.
- [[system/rules/core/timezone-and-local-day-boundary]] bestimmt den Bewertungszeitpunkt.
- scheduled jobs zeigt den gewünschten Schedulerzustand; cron jobs den beobachteten Zustand.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
