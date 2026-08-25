---
schema_version: pos-v1
id: 019ff59c-3043-7a91-a254-bfff792b0aa3
type: rule
title: "Material Run Receipt Retention"
created: 2026-08-12
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Material Run Receipt Retention

## Rule

Ein Automation Run erhält genau dann einen dauerhaften Einzelbeleg, wenn sein Ergebnis materiell, fehlerhaft, offen, extern mutierend oder ausdrücklich auditpflichtig ist. Ein erfolgreicher inhaltsleerer Routine-Run wird ausschließlich im technischen Producer-State und im Automation Day Summary nachgewiesen.

## Scope and Trigger

Die Regel gilt für jeden manuellen, geplanten, event-, webhook- oder backfill-getriggerten Lauf, der PersonalOS-Quellen liest, PersonalOS mutiert, externe Systeme prüft oder externe Seiteneffekte ausführt.

## Required Behavior

- Einzelbeleg schreiben bei fachlicher Änderung, externer Mutation, `partial`, `failed`, `stale`, Deferred/Pending, Source Gap oder konkret benanntem Auditbedarf.
- Keinen Einzelbeleg schreiben, wenn der Lauf vollständig erfolgreich war und weder neue Evidenz noch Änderung, offene Arbeit, Warnung oder externe Mutation erzeugte.
- Jeden abgeschlossenen Lauf atomar im technischen State zählen und Cursor, Coverage sowie Freshness aktualisieren.
- Pro Producer und Kalendertag genau ein Day Summary führen, das Gesamtzahl, Routine-No-ops, materielle Runs, Fehler/offene Zustände und Links zu Einzelbelegen enthält.
- Tagesaggregate, Einzelbelege und technischer State dürfen keine fachliche Current Truth duplizieren.
- No-op ist ein Verarbeitungsergebnis, keine Activity und kein Interaction Event.

## Exceptions

Eine bindende gesetzliche, vertragliche oder sicherheitsbezogene Einzelrun-Pflicht darf die Routine-No-op-Unterdrückung überschreiben. Der Einzelbeleg verwendet dann `run_outcome: audit-no-op` und benennt den konkreten Grund in `retention_reason`. Eine pauschale Vorsichtsformel genügt nicht.

Ein selbstbeobachtender Git-Backup-Writer wie `vault-autocommit` führt für Routine-No-ops keinen Markdown-Day-Summary. Dessen bloße Änderung wäre selbst eine neue zu sichernde Vault-Mutation und würde eine endlose Kette künstlicher Backup-Commits erzeugen. Der Writer zählt Routine-No-ops deshalb ausschließlich atomar im externen Runtime-State und persistiert nur materielle, partielle oder fehlgeschlagene Runs als `automation-run-receipt`. Diese Ausnahme gilt nur, wenn der Day-Summary selbst den vom Producer beobachteten Mutationsbestand verändern würde; andere Producer dürfen sie nicht übernehmen.

Ein untergeordneter Multi-Host-Snapshot-Collector ist kein zweiter fachlicher Automation-Writer. Er aktualisiert ausschließlich den eigenen kanonischen Host-Snapshot. Der benannte zentrale Aggregator besitzt Receipts und Day Summary des Gesamt-Producers. Dadurch schreiben Arbeitsrechner und Service-Host keine konkurrierenden Tagescontainer und beobachteter Host-State wird nicht als zweite Automation-Wahrheit dupliziert.

## Verification

- Der Writer-Test beweist für denselben Producer je einen unterdrückten Routine-No-op und einen persistierten materiellen oder fehlerhaften Run.
- Die Summe aus Day Summary und technischem State stimmt mit der Zahl abgeschlossener Runs überein.
- Jeder verlinkte Einzelbeleg löst auf; Routine-No-op-Runs erzeugen weder Automation Receipt noch Daily Activity Contribution.
- Cursor und Freshness dürfen nur nach vollständiger Coverage oder explizitem offenen Status fortgeschrieben werden.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
