---
schema_version: pos-v1
id: 019ff1bc-2b53-7cc7-863e-7af9861468fe
type: template
title: "Template: Capture"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/core/capture-retention-und-promotion]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
target_profile_key: capture
---

# Template: Capture

## Template Contract

Normative Instanzvorlage für erhaltenswerten Input, dessen dauerhafter Owner oder fachliche Bedeutung noch nicht sicher bestimmt ist.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
input_kind: <input_kind>
---

# <title>

## Current Truth

<current_truth>

## Original Input

<original_input>

## Source Basis

<source_basis>

## Processing and Routing

<processing_and_routing>

## Retention

<retention>

## Timeline

- **<date>** | Capture created.
```

## Usage

- Nicht für jeden Chatgedanken anlegen. Wenn Owner und Delta klar sind, direkt zum kanonischen Owner routen.
- Nur ungeklärten, aber erhaltenswerten Input unter `inbox/captures/<uuid>.md` stagen.
- `unprocessed` bewahrt den Input unverändert beziehungsweise verlustfrei.
- `staged` folgt erst nach einer abgeschlossenen Triage und hält das konkrete verbleibende Owner-, Bedeutungs-, Reifegrad- oder Scope-Gate fest.
- `processed` benötigt `processing_outcome` und `retention_disposition`; alle materiellen Outputs oder begründeten No-ops werden im Body verlinkt. Partial Failure bleibt `staged`.
- Nach grünem Postflight wird ein `processed` Capture im selben Verarbeitungslauf gelöscht. Dauerhaft nötige Evidence oder Receipts müssen vorher beim richtigen Owner liegen; der Inbox-Capture selbst bleibt nie dauerhaft bestehen.
- Secrets werden niemals übernommen. Große oder binäre Quellen erhalten bei Bedarf einen stabilen externen Pointer.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
