---
schema_version: pos-v1
id: 01a0011a-d991-721b-bea4-c56b74e213ea
type: template
title: "Template: Data Model Document"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/domain-ownership-and-admission]]"]
target_profile_key: data-model-document
---

# Template: Data Model Document

## Template Contract

Instanzvorlage für eine menschlich lesbare, normative Erläuterung des maschinenlesbaren Datenmodells. Der konkrete Body folgt seinem `document_kind`; YAML-Registry, Profile und Module bleiben die maschinenlesbare Autorität.

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
decision_refs: <decision_refs>
document_kind: <document_kind>
---

# <title>

## Current Truth

<current_truth>

## Model

<human_readable_model>

## Timeline

- **<date>** | Dokument angelegt oder semantisch geändert.
```

## Usage

Nur für `frontmatter.md`, `governance.md` und `legacy-mapping.md` im kanonischen Datenmodellordner. Diese drei Dokumente teilen normative menschliche Lesbarkeit, besitzen aber bewusst unterschiedliche Bodygliederungen. Neue Dokumentarten rechtfertigen weder automatisch einen neuen Enumwert noch einen freien Datenmodell-Dokumentordner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
