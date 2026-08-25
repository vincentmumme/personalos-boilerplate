---
schema_version: pos-v1
id: 019fec8b-0c07-7146-af56-ecfe0c5c627c
type: runbook
title: "PersonalOS Mutation"
created: 2026-08-10
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/contracts/core/internal-links-and-path-mutations]]", "[[system/conventions/core/record-naming-and-temporal-paths]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
---

# PersonalOS Mutation

## Purpose

Dieses Runbook führt einen autorisierten POS-Write vom fachlichen Intent bis zum geprüften Ergebnis aus, ohne einen zusätzlichen Writer-Skill vorauszusetzen.

## Trigger

Es gilt, sobald ein Agent oder owning Skill eine PersonalOS-Datei erstellen, editieren, verschieben, löschen, anhängen oder materiell neu schreiben soll.

## Preconditions

- User-Intent und Source-Basis sind verstanden.
- Der spezifische owning Skill oder direkte fachliche Owner ist bestimmt.
- Mutationstyp, Zielbereich und erforderliche Freigabe sind bekannt.
- Bei neuer Wahrheit existiert eine Propagation Map mit plausiblen Update-, Reference-, No-op-, Stage- und Ask-Zielen.
- Für neue `pos-v1`-Records sind writable Profile, kanonisches Template und Zielpfad vorhanden.
- Ein passender deterministischer und semantischer Verification-Pfad ist bekannt.

## Procedure

1. Über Resolver und [[system/frameworks/core/context-routing-and-truth-propagation]] den spezifischen Owner und alle materiell plausiblen Nachbarowner bestimmen.
2. Zielrecords, Profile, Templates, direkte `system_refs` und die kleinste ausreichende fachliche Umgebung vollständig lesen.
3. Risiken, Freigaben, externe Auswirkungen, Move-/Delete-Folgen und Link-/Backlink-Bedarf prüfen. Bei Moves oder Renames UUID, alten und neuen Pfad, eingehende Links, Consumer, Redirect-Bedarf und Recovery vor dem Write inventarisieren.
4. Neue `pos-v1`-Records mit der Registry-Runtime rendern und vor der Propagation validieren. Fehlt ein Contract, Profile, Feld oder Template, den Write stoppen und zuerst ein Admission-Paket routen.
5. Die Mutation eng, vollständig und ausschließlich in den ausgewählten Ownern durchführen. Moves und Renames aktualisieren kontrollierbare Links im selben Slice; abgeleitete Views werden zuletzt neu gebaut. Current Truth bei State-Änderungen neu synthetisieren; Timeline nur für echte Events oder materielle Dateiänderungen ergänzen.
6. Geänderte, erstellte, verschobene und gelöschte Dateien explizit erfassen. Plausible No-op-, Stage- und Ask-Ziele samt Grund festhalten.
7. Owner-spezifische Tests, Registry-/Generated-Checks und [[system/checks/core/personalos-mutation-postflight]] ausführen.
8. Failures beheben oder blockierend berichten. Warnungen, Partial Writes und noch nicht migrierte Legacy-Grenzen sichtbar benennen.

## Verification

Der Postflight erhält die explizite Dateiliste statt eines unsicheren Dirty-Tree-Diffs. Er prüft mindestens Shape, Owner, Provenance, Links, Konfliktmarker, Propagation, Current Truth, Timeline, Action-Grenze und Generated Drift. Bei neuen oder geänderten Systemartefakten werden Registry, Fixtures, Generated Views und Consumer-Abhängigkeiten zusätzlich geprüft.

Ein grüner Scriptlauf allein schließt einen bedeutungsverändernden Write nicht ab; die semantische Routingentscheidung muss ebenfalls als korrekt beurteilt sein.

## Escalation

- Bei unklarem Owner oder Reifegrad: kontrolliert stagen oder {{user_name}} fragen.
- Bei fehlendem Profile oder Template: Schema Admission vor fachlichem Write.
- Bei widersprüchlichen Normen: Write blockieren und Supersession-/Propagation-Entscheidung vorbereiten.
- Bei Partial Write: keine Erfolgsmeldung; geänderte und nicht geänderte Ziele exakt benennen.
- Bei Move oder Delete kanonischer Wahrheit: [[system/contracts/core/internal-links-and-path-mutations]] anwenden und Linkplan, Recovery-Pfad sowie geltende Freigabe verlangen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
