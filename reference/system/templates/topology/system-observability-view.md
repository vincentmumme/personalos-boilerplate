---
schema_version: pos-v1
id: 019ffbfe-753d-7566-bd36-8398f695abf2
type: template
title: "Template: System Observability View"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/principles/core/system-truth-is-self-describing]]"]
target_profile_key: system-observability-view
---

# Template: System Observability View

## Template Contract

Normative Instanzvorlage für das registrierte `system-observability-view`-Profil.

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
canonical_system_ref: "[[system/truth-systems/personalos]]"
authority_scope: <authority_scope>
observability_scope: <observability_scope>
observed_at: <observed_at>
observability_source_refs: <observability_source_refs>
---

# <title>

## Purpose

<purpose>

## Observed Scope

<observed-scope>

## Desired versus Observed

<desired-versus-observed>

## Sources and Freshness

<sources-freshness>

## Limitations

<limitations>
```

## Usage

Nur am durch das Profil zugelassenen Systempfad verwenden; fachliche Wahrheit und Secret-Werte bleiben bei ihren eigenen Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
