---
schema_version: pos-v1
id: 019fec5e-7fa5-719f-a464-01b93ec2e741
type: template
title: "Template: pos-v1 Redirect"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: redirect
---

# Template: pos-v1 Redirect

## Template Contract

Normative Instanzvorlage für einen temporären Continuity Pointer. Ein Redirect besitzt keine fachliche Wahrheit am Altpfad.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
redirect_target_ref: "<redirect_target_ref>"
---

# <title>

## Target

Der kanonische Record liegt unter <redirect_target_ref>.

## Continuity

Dieser Record erhält ausschließlich bestehende Links während der kontrollierten Migration und besitzt keine eigene fachliche Wahrheit.

## Removal Prerequisite

Dieser Redirect wird entfernt, sobald alle kontrollierbaren aktiven Consumer den kanonischen Zielpfad verwenden und der repositoryweite Link-Postflight grün ist.
```

## Usage

Redirects werden nur bei echtem Kontinuitätsbedarf erzeugt, nie als zweiter Wahrheitsowner verwendet und besitzen immer eine prüfbare Entfernungsvoraussetzung.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
