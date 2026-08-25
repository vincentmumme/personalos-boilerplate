---
schema_version: pos-v1
id: 019fec5e-7f7a-7e41-a596-1c433e0cdb68
type: template
title: "Template: pos-v1 Working Note"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: working-note
---

# Template: pos-v1 Working Note

## Template Contract

Normative Instanzvorlage für das registrierte Primary Profile `working-note`. Working Notes besitzen Working Truth und keine konkurrierende fachliche Current Truth.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
project_ref: "<project_ref>"
---

# <title>

## Working Truth

<working_truth>

## Re-entry

<re_entry>
```

## Usage

Working Notes werden nur in einem registrierten Work-Kontext und ohne konkurrierende Current Truth erstellt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
