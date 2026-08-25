---
schema_version: pos-v1
id: 01a0016e-6141-7feb-a033-b7026a24272a
type: template
title: "Template: Knowledge Assessment"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
target_profile_key: knowledge-assessment
---

# Template: Knowledge Assessment

## Template Contract

Zeitgebundene Qualitäts-, Reife- oder Migrationsbewertung. Ein Assessment empfiehlt Änderungen, besitzt aber nicht die geprüfte Knowledge Truth.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: knowledge-assessment
title: "<title>"
created: <date>
updated: <date>
lifecycle: active
topic_ref: "[[knowledge/topics/<topic>/<topic>]]"
assessment_kind: <assessment_kind>
assessment_outcome: <assessment_outcome>
---

# <title>

## Assessment

<scope and method>

## Findings

<findings>

## Recommendations

<bounded recommendations>

## Sources

<scanned records and evidence>

## Re-entry

<next assessment condition>
```

## Usage

Librarian- und Lint-Berichte verwenden dieses Profil. Änderungen an Articles bleiben ein gesonderter, ausdrücklich gerouteter Compile-Schritt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
