---
schema_version: pos-v1
id: 019fec59-ed35-751a-92b8-c995c1d24e8c
type: template
title: "Template: Principle"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
target_profile_key: principle
---

# Template: Principle

## Template Contract

Instanzvorlage für eine langfristige normative Ableitungsgrundlage. Feld- und Pfadregeln besitzt ausschließlich das Profile `principle`.

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
decision_refs: <decision_refs>
---

# <title>

## Principle

<principle>

## Rationale

<rationale>

## Implications

<implications>

## Boundaries

<boundaries>

## Change History

- **<date>** | Principle created.
```

## Usage

Nur für wenige dauerhafte Grundlagen verwenden, aus denen nachgelagerte Normen ableitbar sind.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
