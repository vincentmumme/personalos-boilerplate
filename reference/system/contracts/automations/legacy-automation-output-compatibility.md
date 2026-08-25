---
schema_version: pos-v1
id: 01a001e5-56b1-7ca6-850d-2b7f0c493a35
type: contract
title: "Legacy Automation Output Compatibility"
created: 2026-06-03
updated: 2026-08-22
lifecycle: retired
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Legacy Automation Output Compatibility

## Contract

Dieser stillgelegte Vertrag dokumentiert ausschließlich den historischen Legacy-Envelope früherer News-/Creator-Producer. Er besitzt keine Write-Autorität. Alle aktiven Producer verwenden einen Automation-Hauptrecord, technische State-Erfassung, eine kompakte Day Summary und nur bei materiellem, fehlerhaftem, offenem, extern mutierendem oder auditpflichtigem Ausgang einen einzelnen Run Receipt.

Historische Bestände können folgenden früheren Envelope tragen:

```yaml
schema_version: pos-gbrain-v1
type: source
pos_domain: automations
subtype: automation-output
role: automation-output
status: success
title: "<Producer>: <YYYY-MM-DD>"
automation: <producer-slug>
skill: <producer-slug>
run_date: <ISO timestamp with timezone>
run_status: success
run_trigger: scheduled
briefing_include: true
briefing_section: news
summary: "<kurze Karte>"
priority: normal
updated: <YYYY-MM-DD>
tags: [automation-output]
```

`status` muss `run_status` spiegeln. Zugelassene Run-Zustände sind `success`, `partial`, `failed`, `error`, `stale` und `empty`; `run_trigger` verwendet `scheduled`, `manual`, `webhook` oder `backfill`.

## Scope

Der Vertrag gilt nur als Lesekontext für bestehende datierte Legacy-Outputs. Historische Outputs bleiben lesbare Evidenz, autorisieren aber keinen neuen Writer. Morning Briefing, Signalquellen, Systemassessments, Health, Knowledge und alle anderen aktiven Producer fallen ausschließlich unter den Zielvertrag.

## Invariants

1. Keine neue Automation übernimmt diesen Legacy-Envelope.
2. Producer-Output ist Evidence oder abgeleitete Lieferung und niemals zweite fachliche Current Truth.
3. Secrets, Tokens, vollständige Mail-Bodies, Chatlogs, private Zahlungsdaten und unnötige Rohdaten bleiben ausgeschlossen.
4. Ein erfolgreicher leerer Run erzeugt nach dem Zielvertrag keinen individuellen Receipt und keine Daily Activity.
5. Fachliche Deltas werden zu ihren kanonischen Ownern propagiert; das Output-Archiv ersetzt diese Propagation nicht.
6. `status == run_status`, Producer-Slug und datierter Outputpfad werden vor Abschluss des Runs zurückgelesen und geprüft.

## Interfaces

- index navigiert die Automation Registry, ohne Outputs zu enumerieren.
- [[system/frameworks/interactions/signal-evidence-und-processing]] definiert Source, Evidence, Analysis, Propagation und Receipt.
- [[system/rules/automations/material-run-receipt-retention]] definiert die Ziel-Retention.
- Das Morning Briefing liest fachliche Owner, Day Summaries und nur solange nötig explizit zugelassene Legacy-Outputs; es ist kein Scraper und kein zweiter Output-Owner.

## Compliance

Neue Writes gegen diesen Vertrag sind nicht compliant. Historische Dateien werden nicht allein wegen ihres Envelopes umgeschrieben oder gelöscht; ihre Klassifikation, Unveränderlichkeit und Nicht-Autorität bleiben durch Compatibility Checks abgesichert.

## Evolution

Der Vertrag bleibt als `retired`-Beleg erhalten, solange historische Outputs oder Consumer seine Semantik benötigen. Der Redirect unter `automations/automation-output-contract.md` darf erst nach einem belegten Link-Postflight entfernt werden.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
