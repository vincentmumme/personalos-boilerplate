---
schema_version: pos-v1
id: 019fec5e-7fd1-76ad-8560-e753b61f03ca
type: template
title: "Template: pos-v1 Truth System"
created: 2026-08-10
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: truth-system
---

# Template: pos-v1 Truth System

## Template Contract

Normative Instanzvorlage für registrierte Systeme, die kanonische Wahrheit halten oder auf sie verweisen.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
system_kind: <system_kind>
default_timezone: <default_timezone>
---

# <title>

## Current Truth

<current_truth>

## Scope

<scope>

## Authority

<authority>

## Interfaces

<interfaces>

## Timeline

- **<date>** | Truth System record created.
```

## Usage

Nur Systeme mit einer klaren kanonischen Authority- und Interface-Grenze werden registriert. Ein System, das den lokalen Zeitfallback besitzt, deklariert ihn als IANA-Zeitzone in `default_timezone`; andere Truth Systems lassen das Feld weg.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
