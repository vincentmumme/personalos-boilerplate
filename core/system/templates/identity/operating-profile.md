---
schema_version: pos-v1
id: 019ffb77-265c-790b-9bc8-23841999fd48
type: template
title: "Template: Identity Operating Profile"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-operating-profile
---

# Template: Identity Operating Profile

## Template Contract

Agentisch nutzbarer, dauerhafter Kontext darüber, wie das System-Subject denkt, lernt, kommuniziert und arbeitet.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-operating-profile
title: "Operating Profile"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Operating Profile

## Current Truth
<current_truth>

## Traits and Preferences
<traits>

## Thinking and Decision-Making
<thinking>

## Learning
<learning>

## Communication
<communication>

## Work and Execution
<work>

## Helpful Conditions
<helpful_conditions>

## Failure Modes and Friction
<failure_modes>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Stabilen persönlichen Arbeitskontext halten; kurzfristige Zustände und Agentenverhalten besitzen andere Owner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
