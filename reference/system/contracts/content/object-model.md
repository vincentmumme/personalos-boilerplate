---
schema_version: "pos-v1"
id: "01a002b7-e000-738f-a3f0-fb852ebfbf5d"
type: "contract"
title: "ContentOS v1 Object Model"
created: "2026-08-02"
updated: "2026-08-15"
lifecycle: "active"
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: "2.0.0"
---

# ContentOS v1 Object Model

## Contract

### Record Floor

Every materialized ContentOS object is a native `pos-v1` record with the six global foundation fields: `schema_version`, UUIDv7 `id`, registered Primary Profile in `type`, `title`, `created` and `updated`. The admitted Content profile adds only the fields and modules needed by that object. Mutable operational records use `revision`; their workflow state lives in the profile-owned field such as `lifecycle`, `source_state`, `publication_state` or `link_state`.

The UUIDv7 is identity. Readable slugs and paths are locators; titles, provider IDs and URLs are attributes. Relations use typed POS wikilinks and therefore survive readable path changes through the normal link-maintenance contract.

### Objects and Lifecycles

| Object | Primary Profile | State field and lifecycle |
|---|---|---|
| Input | `content-input` | capture metadata; result relations after routing |
| Idea | `content-idea` | `lifecycle`: captured, qualified, selected, converted, parked, archived |
| Source | `content-source` | `source_state`: captured, processing, processed, partial, failed, archived |
| Research Pack | `content-research` | `lifecycle`: draft, in-review, complete, superseded, archived |
| Format, Series, Recipe | `content-format`, `content-series`, `content-production-recipe` | `lifecycle`: draft, active, deprecated, archived |
| Piece | `content-piece` | `lifecycle`: draft through active; cancelled and retired remain explicit |
| Context Pack and Production Spec | `content-context-pack`, `content-production-spec` | locked/approved revisions with supersession |
| Asset Manifest and Production Job | `content-asset-manifest`, `content-production-job` | asset truth and executor-specific work state |
| Version and Publication | `content-version`, `content-publication` | platform package and one real upload |
| Tracking Link and Evidence | `content-tracking-link`, `content-evidence` | placement attribution and normalized observation |
| Knowledge/Learning Candidate | `content-knowledge-candidate`, `content-learning-candidate` | proposed, approved, rejected or superseded |

### Required Relationships

- Piece: `input_refs`, optional `idea_refs`, `source_refs`, `research_refs`, `derived_from`, `format_ref`, `series_ref`, `recipe_refs`.
- Context Pack and Production Spec: exactly one `piece_ref` and their own revision.
- Version: exactly one `piece_ref`, one platform and one publishing account. Several platform Versions may reference the same approved export asset when no platform-specific edit is needed; the Version then records channel packaging, CTA, placement, and measurement differences without fabricating a creative difference.
- Job: exactly one `piece_ref`, one `production_spec_ref`, executor and idempotency key.
- Publication: exactly one `piece_ref` and `version_ref`; live state also requires platform account, URL/native ID and published timestamp.
- Tracking Link: Piece, placement, destination, CTA intents and provider-independent link ID.
- Candidate: Evidence refs and exactly one `target_owner`.

### Versioning and Concurrency

Edits to revisioned Content records increment `revision`. Agents compare the revision they read before writing; mismatches stop with a conflict. Historical Context, Spec, Version, Publication and Evidence revisions are not silently overwritten. Operation retries reuse the same durable UUIDv7 and idempotency key.

### Unknowns

Unknown values are explicit (`unknown`, `unavailable`, `ambiguous`, `not-applicable`) only where the object/state contract permits. Required identity or relationship fields cannot be list-wrapped, empty or guessed.

### Embedded Subrecords

Creative Variants, observations, hypotheses and provider payload details live in typed body sections or companion data unless they need their own approval, Publication, analytics lifecycle or registered Primary Profile. Nested structures are not placed into frontmatter merely for convenience.

### Timeline

- **2026-08-15** - Replaced the retired Content-local schema envelope with admitted POS-v1 Primary Profiles, UUIDv7 identity and typed wikilink relations.
- **2026-08-05** - Clarified that platform identity and measurement require separate Versions even when several Versions reuse the same export asset.
- **2026-08-02** - Established v1 objects, relationships, states and revision rules.

## Scope

ContentOS records, workflows, storage, analytics or capability boundaries defined by this contract.

## Invariants

The global POS-v1 registry owns record shape; this contract owns only Content-domain semantics.

## Interfaces

Consumed through the ContentOS skill and its deterministic validators.

## Compliance

Changes require registry-safe verification and ContentOS semantic tests.

## Evolution

Revise through the ContentOS migration project and preserve explicit supersession.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
