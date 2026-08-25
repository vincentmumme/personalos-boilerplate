---
schema_version: pos-v1
id: 019ffb88-8757-7dbf-8ab1-41e27f114815
type: template
title: "Template: Owner Index"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/conventions/core/index-view-and-discovery]]"]
target_profile_key: owner-index
---

# Template: Owner Index

## Template Contract

Portabler kuratierter Einstieg eines kanonischen Root- oder Section-Owners ohne eigene fachliche Current Truth.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: owner-index
title: "<title>"
created: <date>
updated: <date>
index_scope: <index_scope>
---

# <title>

## Purpose

<purpose>

## Ownership and Boundaries

<ownership_and_boundaries>

## Navigation

<curated_navigation>

## Maintenance

Dieser Index enthält nur stabile Navigation und Ownergrenzen. Vollständige Listen, Live-Status, Tasks und fachliche Current Truth werden nicht manuell hier gepflegt.
```

## Usage

Jeder kanonische Root verwendet einen Owner Index. Section-Indizes entstehen nur bei einer eigenständig navigierbaren Boundary; Jahres-, Technik- und Leaf-Ordner erhalten standardmäßig keinen Index.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
