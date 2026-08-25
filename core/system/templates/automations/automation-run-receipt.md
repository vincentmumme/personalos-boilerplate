---
schema_version: pos-v1
id: 019ff59c-3155-7710-9c2a-c46be3100f51
type: template
title: "Template: Automation Run Receipt"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/rules/automations/material-run-receipt-retention]]"]
target_profile_key: automation-run-receipt
---

# Template: Automation Run Receipt

## Template Contract

Einzelbeleg ausschließlich für materielle, fehlerhafte, offene, extern mutierende oder konkret auditpflichtige Automation Runs.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
run_id: <run_id>
run_started_at: <run_started_at>
run_ended_at: <run_ended_at>
run_outcome: <run_outcome>
run_trigger: <run_trigger>
producer_skill_ref: "<producer_skill_ref>"
retention_class: material-run
---

# <title>

## Run Summary

<what the run did and why this individual receipt is retained>

## Coverage

<source window, accounting and freshness>

## Propagation

<changed, referenced and no-op owners>

## Errors and Pending

<failures, deferred work, pending evidence or none>

## Evidence

<interaction and domain evidence links>

## Corrections

None.
```

## Usage

Routine-No-op ist kein zulässiger normaler `run_outcome`. Eine auditpflichtige Ausnahme verwendet `audit-no-op` und ergänzt `retention_reason`.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
