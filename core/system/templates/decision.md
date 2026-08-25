---
schema_version: pos-v1
id: 019ff23d-f43a-709f-9278-cedc9d2e4395
type: template
title: "Template: Decision"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/integritaet-von-decision-records]]", "[[system/conventions/core/record-naming-and-temporal-paths]]", "[[system/contracts/core/internal-links-and-path-mutations]]"]
target_profile_key: decision
---

# Template: Decision

## Template Contract

Instanzvorlage für einen bestätigten, semantisch unveränderlichen Decision Record. Offene Optionen und Decision Gates verwenden dieses Template nicht.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
decision_state: active
decision_confidence: <decision_confidence>
decided_on: <decided_on>
decided_by_refs: <decided_by_refs>
affected_owner_refs: <affected_owner_refs>
---

# <title>

## Decision

<the confirmed choice>

## Context

<situation and decision boundary at that time>

## Why

<reasoning>

## Alternatives

<real alternatives and why they lost>

## Consequences

<downstream effects and propagation>

## Reconsider When

<conditions for re-evaluation, supersession or reversal>

## Affected Owners

<links and propagation outcome>

## Sources

<source links or traceable decision context>

## Corrections

<dated non-semantic repairs, or "None.">
```

## Usage

The target path is `decisions/<year>/YYYY-MM-DD-<slug>.md`, using `decided_on`. A new direction creates a new Decision with `supersedes_decision_refs` or `reverses_decision_refs`; the old Decision becomes terminal and receives `successor_decision_ref`. Resulting Current Truth is propagated to every affected owner before the write is complete.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
