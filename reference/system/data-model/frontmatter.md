---
schema_version: pos-v1
id: 01a0011a-da94-7761-9f14-d289f9e59f9d
type: data-model-document
title: "Frontmatter Profile"
created: 2026-08-06
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
document_kind: frontmatter-guide
---

# Frontmatter Profile

## Current Truth

Der normative Frontmatter-Vertrag ist `pos-v1`. Jede POS-verwaltete Markdown-Datei besitzt genau diese Foundation: `schema_version`, lowercase UUIDv7-`id`, registriertes Primary Profile `type`, `title`, `created` und `updated`. `status`, `role`, `pos_domain`, Tags, Sources, Lifecycle und Domainfelder sind nicht universell. Bei `SKILL.md` liegt dieselbe Foundation runtimebedingt mit `pos_` präfixiert innerhalb von `metadata`; `name` und `description` bleiben der äußere Runtime-Vertrag.

Genau ein Primary Profile komponiert Page Shape, kanonischen Owner, erlaubte Module, Pflicht-/optionale Felder, Pfad, Body Sections, State Machine, Relations und Template. Jedes Feld wird genau einmal in Foundation, Modul oder Profile definiert. Die maschinenlesbare Wahrheit liegt in `registry.yaml` und den referenzierten YAML-Dateien; dieses Dokument ist die menschliche Einordnung.

Die UUIDv7 ist die stabile Record-Identität; Pfad und Dateiname sind lesbare Navigation. Konkrete Profile folgen [[system/conventions/core/record-naming-and-temporal-paths]]. Interne Relations bleiben pfadqualifizierte Obsidian-Wikilinks und folgen bei Moves [[system/contracts/core/internal-links-and-path-mutations]].

## Body over metadata

Current Truth, Timeline, Entscheidungen, Risiken, Begründungen und andere Narrative gehören in den Markdown-Body. Große oder tief strukturierte Daten verwenden Companion Data; Binär- und Großassets bleiben extern mit manifestierten Pointern. Frontmatter hält kleine atomare Routing-, State-, Relationship-, Temporal-, Query- und Validation-Werte.

## Profile rule

Neue Felder, Module oder Profile durchlaufen die zentrale Admission-/Evolution-Regel und werden nie ad hoc in einer Instanz erfunden. Optionale leere Werte, `null`, leere Listen, freie POS-Maps und das unqualifizierte Feld `status` sind im Zielcontract verboten. Die registrierte Skill-Envelope ist keine freie POS-Map: unbekannte `pos_*`-Felder werden abgelehnt; fremde Runtime-Namensräume unter `metadata` besitzen keine POS-Autorität.

`pos-gbrain-v1` bleibt ausschließlich als zugelassener Lesevertrag für klassifizierte historische Evidenz, technische Historie und unveränderliche Referenzbestände erhalten. Es autorisiert weder neue Records noch neue Legacy-Writer. Neue Writes sind nur für Profile erlaubt, deren zentraler `profile_states`-Eintrag `pilot` oder `active` ist.

Der Registry-State `pilot` ist der aktuelle schreibbare Reifegrad des freigegebenen POS-v1-Vertrags und keine offene Bestandsmigration. Eine spätere Promotion einzelner Profile auf `active` folgt den Kriterien aus `governance.yaml` und verändert weder Recordidentität noch Ownergrenze.

## Domain transition rule

Der globale Vertrag gilt für jede neue oder aktiv fortgeschriebene POS-verwaltete Markdown-Datei. Alle heute aktiven Domains besitzen ihr zugelassenes Admission-/Cutover-Paket. Historische Dateien dürfen in ihrem manifestierten Legacy-Envelope lesbar bleiben, wenn sie keine aktive Wahrheit und keinen Writervertrag besitzen; Dual Writes bleiben verboten.

ContentOS hat diesen vollständigen Domaincutover am 2026-08-15 abgeschlossen. Alle aktiven Content-Records komponieren die sechs-Felder-Foundation mit registrierten Content Primary Profiles und dem `content-core`-Modul; Templates, Mappings, IDs, Links und Checks liegen in der gemeinsamen POS-v1-Schicht. [[system/contracts/content/contentos-pos-v1-transition]] bleibt ausschließlich historischer Cutover-Beleg und besitzt keine aktive Write-Autorität.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
