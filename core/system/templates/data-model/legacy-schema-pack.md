---
schema_version: pos-v1
id: 01a0011a-d9e9-7043-bf25-f25b52dd78e2
type: template
title: "Template: Legacy Schema Pack"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: legacy-schema-pack
---

# Template: Legacy Schema Pack

## Template Contract

Instanzvorlage für die befristete menschliche Einordnung eines weiterhin lesbaren, aber nicht mehr beschreibbaren Legacy-Schema-Packs.

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
---

# <title>

## Current Truth

<current_truth>

## State

<machine_pack_and_current_owner>

## Open Threads

<removal_prerequisite>

## See Also

<migration_and_contract_refs>

## Timeline

- **<date>** | Legacy-Referenz angelegt oder geändert.
```

## Usage

Neue Records dürfen niemals aus diesem Pack geschrieben werden. `read-only` hält kontrollierte Legacy-Kompatibilität; `retired` ist erst nach null aktiven Consumern und Recovery-Beleg zulässig.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
