---
schema_version: pos-v1
id: 019ff59c-30fa-779e-98ea-7b5a8e92258d
type: template
title: "Template: Source Evidence"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]"]
target_profile_key: source-evidence
---

# Template: Source Evidence

## Template Contract

Unveränderlicher oder korrekturgebundener redigierter Beleg für ein Interaction Event oder einen Conversation Stream.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
evidence_kind: <evidence_kind>
evidence_captured_at: <evidence_captured_at>
source_system: <source_system>
source_ref: <source_ref>
interaction_ref: "<interaction_ref>"
redaction_mode: <redaction_mode>
---

# <title>

## Evidence Summary

<compact description of the captured evidence>

## Source Boundary

<what this evidence proves and does not prove>

## Evidence

<redacted source material or stable asset pointer>

## Corrections

None.
```

## Usage

Atomare Evidence verwendet UUIDv7-Dateinamen im `evidence/`-Modul des Interaction Owners. Binärdateien werden nicht eingebettet.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
