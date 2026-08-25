---
schema_version: pos-v1
id: 01a0015e-8a7b-730a-a069-6af0bb5d73ac
type: template
title: "Template: Skill Reference"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/capability-interface]]"]
target_profile_key: skill-reference
---

# Template: Skill Reference

## Template Contract

Skilllokale, nicht ausführbare Referenz für Kalibrierung, Pattern Memory, Providerdetails, Schemas, Beispiele oder eingefrorene Kompatibilität. Allgemeine Regeln und Konventionen bleiben unter `/system`.

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
owning_skill_ref: "<owning_skill_ref>"
reference_kind: <reference_kind>
---

# <title>

<skill-specific reference content>
```

## Usage

Der Pfad liegt unter `skills/<skill>/references/`. Eine Referenz besitzt weder Routing-Autorität noch allgemeine Systemnorm. Wird ihr Inhalt allgemein gültig, wird er zum passenden Owner unter `/system` propagiert und die Referenz nur als lokale Anwendung oder Herkunft behalten.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
