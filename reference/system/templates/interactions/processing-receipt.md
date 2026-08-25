---
schema_version: pos-v1
id: 01a0013d-1bac-7997-a73c-908ac496a420
type: template
title: "Template: Processing Receipt"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/frameworks/core/capture-retention-und-promotion]]"]
target_profile_key: processing-receipt
---

# Template: Processing Receipt

## Template Contract

Unveränderlicher Verarbeitungsbeleg für einen Interaction-Lauf mit Multi-Owner-Propagation, Partial Failure oder konkretem Auditbedarf. Source Evidence, Analyse und fachliche Wahrheit werden nicht kopiert.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
receipt_kind: <receipt_kind>
receipt_outcome: <receipt_outcome>
processed_at: <processed_at>
verification_result: <verification_result>
producer_skill_ref: "<producer_skill_ref>"
interaction_ref: "<interaction_ref>"
evidence_refs: <evidence_refs>
affected_owner_refs: <affected_owner_refs>
---

# <title>

## Processing Summary

<what was processed and why a durable receipt is required>

## Coverage

<input, evidence and semantic scope>

## Propagation

<changed, referenced, staged, asked and no-op owners>

## Verification

<structural, semantic and mutation postflight>

## Errors and Pending

<partial failures, unresolved evidence or none>

## Corrections

None.
```

## Usage

Kein Receipt für einen gewöhnlichen erfolgreichen Single-Owner-No-op. Die Datei liegt als UUID unter dem `processing/`-Modul des Interaction Owners. Automatisierte Läufe verwenden weiterhin `automation-run-receipt` und `automation-day-summary` statt dieses Profils.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
