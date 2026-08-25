---
schema_version: pos-v1
id: 01a0011a-d9ba-7f7a-a777-2fe9c4d7fef9
type: template
title: "Template: Data Model Changelog"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/data-model/governance]]"]
target_profile_key: data-model-changelog
---

# Template: Data Model Changelog

## Template Contract

Instanzvorlage für das append-only Release- und Korrekturprotokoll der zentralen Datenmodell-Registry.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
---

# <title>

## <date> · Registry <version>

- <decision-bearing change>
- <migration or compatibility consequence>
- <verification evidence>
```

## Usage

Neueste Einträge stehen oben. Bestehende Einträge werden nicht still umgeschrieben; sachliche Korrekturen werden als neuer Eintrag kenntlich gemacht. Der Changelog ist ein Release-Log und keine zweite Registry.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
