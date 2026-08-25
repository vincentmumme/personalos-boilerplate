---
schema_version: pos-v1
id: 019fecaa-1257-7094-84fd-ace36e97a088
type: runbook
title: "Test Before Bulk"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/runbooks/core/personalos-mutation]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Test Before Bulk

## Purpose

Dieses Runbook verhindert, dass breite PersonalOS-Operationen einen unbewiesenen Write-Vertrag, Producer-Fehler oder falsches Routing vervielfachen.

## Trigger

Es gilt für Imports, Migrationen, Enrichment, Archive/Cleanup, Massenänderungen an Skills oder Normen, neue Producer und andere Operationen, die mehrere heterogene Records oder wiederholte Writes betreffen.

## Preconditions

- Owning Skill, Source Set, Write Scope und erwartete Zielprofile sind bekannt.
- Die Operation besitzt Stop Conditions und einen expliziten Verification-Pfad.
- Ein repräsentativer Slice von drei bis fünf Fällen deckt normale Fälle, relevante Edge Cases und mindestens einen erwartbaren Failure-/No-op-Fall ab.
- Cursors oder `last_successful_*`-State können bis zum vollständigen Erfolg unverändert bleiben.

## Procedure

1. Owning Skill, Systemverträge, Profile, Templates und relevante Checks lesen.
2. Drei bis fünf repräsentative Items auswählen und ihre erwarteten Owner sowie Outputs vor dem Write festhalten.
3. Nur diesen Slice ausführen.
4. Tatsächliche Dateien, Routing, Current Truth, Provenance, Links und Producer-Ausgabe inspizieren.
5. Owning Skill, Script, Prompt, Template oder Check korrigieren, wenn der Slice den Vertrag nicht erfüllt; nicht nur die fehlerhaften Instanzen manuell reparieren.
6. Den Slice erneut vollständig ausführen und verifizieren.
7. Erst nach grünem Slice die breite Operation in kontrollierbaren Batches starten.
8. Bei wiederholten Findings, unbekannten Shapes, Owner-Ambiguität oder wachsender Fehlerrate stoppen; Cursors und Completion State nicht vorziehen.

## Verification

- Der repräsentative Slice besteht seine owner-spezifischen Checks und [[system/checks/core/personalos-mutation-postflight]].
- Geänderte Dateien und No-op-Fälle sind explizit bekannt.
- Producer und wiederholbare Ausführung wurden korrigiert, nicht nur einzelne Outputs.
- Der Bulk-Lauf besitzt eine Batchgröße, Stop Condition und einen Wiederaufnahmezustand.
- Collector und semantische Verarbeitung sind vollständig, bevor Cursors oder Completion State fortgeschrieben werden, sofern kein ausdrücklich definierter Archive-only-Modus gilt.

## Escalation

- Unklare Owner, neue Record-Shapes oder fehlende Profile stoppen den Bulk und werden als Admission-/Decision-Gate geroutet.
- Nicht repräsentative oder nicht prüfbare Testfälle erlauben keinen breiten Lauf.
- Ein Failure nach Start des Bulks stoppt die nächste Batch; bereits geschriebene Files werden als Partial Write inventarisiert und geprüft.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
