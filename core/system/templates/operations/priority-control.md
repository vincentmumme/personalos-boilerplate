---
schema_version: pos-v1
id: 01a0251c-9e3a-731c-8fb8-340619cc7014
type: template
title: "Template: Priority Control"
created: 2026-08-21
updated: 2026-08-21
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/operations/priority-dashboard]]"]
target_profile_key: priority-control
---

# Template: Priority Control

## Template Contract

Normative Instanzvorlage für {{user_name}}s befristete manuelle Prioritätsrichtung. Der Record ordnet oder unterdrückt ausschließlich Links auf kanonische Actions; er besitzt weder Task-Inhalt noch Completion- oder Lifecycle-Wahrheit der verlinkten Records.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: priority-control
title: "Priority Control"
created: <date>
updated: <date>
lifecycle: active
priority_control_review_on: <date>
priority_control_expires_on: <date>
priority_focus_areas: ["<focus-area>"]
priority_focus_action_refs: ["[[operations/actions/<uuid>]]"]
priority_ordered_action_refs: ["[[operations/actions/<uuid>]]"]
priority_excluded_action_refs: ["[[operations/actions/<uuid>]]"]
---

# Priority Control

## Current Truth

<short current control state>

## Manual Direction

<why {{user_name}} is temporarily steering focus, order or exclusions>

## Scope and Expiry

<review and expiry boundary; no task state>

## Timeline

- **<date>** | Manual priority direction changed.
```

## Usage

Optionale Listen vollständig weglassen, wenn sie leer sind. Ein aktiver Control-Record benötigt ein Ablaufdatum. Abgelaufene Anweisungen werden vom Dashboard automatisch ignoriert, aber nicht als erledigte Tasks interpretiert. Nach jeder Änderung wird der Dashboard-Rebuild mit `--reason manual-priority-change` ausgeführt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
