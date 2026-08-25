---
schema_version: pos-v1
id: 019ffb77-265c-7d7d-846d-3b61e8e65d85
type: template
title: "Template: Legal Identity"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/identity/identity-subject-and-facets]]"]
target_profile_key: identity-legal
---

# Template: Legal Identity

## Template Contract

Persönliche Legal-Identity-Fakten und offizielle Identifikatoren; keine Secrets, Zahlungsdaten oder vollständigen Dokumentkopien.

## Blueprint

```markdown
---
schema_version: pos-v1
id: <id>
type: identity-legal
title: "Legal Identity"
created: <date>
updated: <date>
lifecycle: active
subject_ref: "<subject_ref>"
---

# Legal Identity

## Current Truth
<current_truth>

## Legal Identity Facts
<legal_facts>

## Residency and Personal Status
<residency>

## Official Identifiers
<identifiers>

## External Document References
<document_refs>

## Sources
<sources>

## Timeline
- **<date>** | Record created.
```

## Usage

Ausweis-, Steuer- oder Sozialversicherungsnummern dürfen bei bewusstem Bedarf im privaten PersonalOS stehen. Passwörter, API Keys, Karten- und Zugangsdaten bleiben im Secrets Manager; Finance- und Company-Wahrheit bleibt bei ihren Ownern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
