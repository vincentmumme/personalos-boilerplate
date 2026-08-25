---
schema_version: pos-v1
id: 019ffbfb-539f-7ba7-ae46-22502b8e2586
type: rule
title: "Template Governance"
created: 2026-08-06
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Template Governance

## Rule

Jedes Template für einen persistierten PersonalOS-Record liegt unter `system/templates/`, gehört genau einem registrierten Zielprofil und wird gemeinsam mit Profile, Fixtures, Validator und Mapping entwickelt.

## Scope and Trigger

Die Regel gilt, sobald ein Skill, Agent, Script oder Mensch wiederholt eine PersonalOS-Datei mit definierter Struktur erzeugt oder materialisiert.

## Required Behavior

- Persistierte Record-Blueprints zentral unter `system/templates/<scope>/...` halten.
- Skills und Writer referenzieren das zentrale Template und dürfen dessen Feld- oder Body-Contract nicht lokal neu definieren.
- Profil, Template, positive und negative Fixture, Validator-Coverage, Legacy-Mapping, Registry-Eintrag und Generated Artifacts atomar ändern.
- Technische Prompts, API-Payloads, Testdaten, Provider-Assets und nicht persistierte Hilfsartefakte dürfen beim owning Skill bleiben.

## Exceptions

Ein skilllokales Artefakt ist nur zulässig, wenn es keinen PersonalOS-Record materialisiert und keine allgemeine POS-Semantik definiert. Ein eingefasstes Markdown-Beispiel ist funktional ein Template, wenn ein Writer es als Blueprint verwendet.

## Verification

- Jeder persistierte Writer nennt sein `template_ref` beziehungsweise leitet den Shape aus dem registrierten Profil ab.
- Kein aktiver Skill hält eine zweite persistierte Record-Vorlage.
- Registry-Build und Zielprofil-Fixtures sind grün.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
