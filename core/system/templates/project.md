---
schema_version: pos-v1
id: 019fec5e-7f4e-797d-ac8f-c5c085e5ad84
type: template
title: "Template: pos-v1 Project"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: project
---

# Template: pos-v1 Project

## Template Contract

Normative Instanzvorlage für das registrierte Primary Profile `project`. Feldregeln und Enums werden nicht hier, sondern in `system/data-model/profiles/project.yaml` definiert.

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
priority: <priority>
workflow: <workflow>
project_phase: <project_phase>
commercial_state: <commercial_state>
sponsor_refs: <sponsor_refs>
human_role: <human_role>
canonical_system_ref: "<canonical_system_ref>"
authority_scope: <authority_scope>
---

# <title>

## Current Truth

<current_truth>

## Outcome and Success Criteria

<outcome_and_success_criteria>

## Scope

<scope>

## Authority and Roles

<authority_and_roles>

## Navigation

<navigation>

## Propagation

<propagation>

## Timeline

- **<date>** | Project record created.
```

## Usage

Neue Project-Hauptrecords werden ausschließlich über Registry und dieses registrierte Template gerendert. `project_phase` und `commercial_state` werden vollständig ausgelassen, wenn die jeweilige Achse für das Project nicht relevant oder noch nicht belegt ist. Leere Platzhalter sind unzulässig.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
