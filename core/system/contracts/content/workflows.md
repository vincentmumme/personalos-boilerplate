---
schema_version: "pos-v1"
id: "01a002b7-e000-79d8-9df1-e43c2a639197"
type: "contract"
title: "ContentOS v1 Workflow Contracts"
created: "2026-08-02"
updated: "2026-08-02"
lifecycle: "active"
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: "1.0.0"
---

# ContentOS v1 Workflow Contracts

## Contract

### Capture

Persist original input and intent before interpretation. Execute only requested extraction. Additional opportunities are suggestions and never canonical truth without confirmation. Capture-only creates no Piece.

### Plan and Create

Guided recommendations create no durable Piece before selection. Quick Create and Publish-first may go directly from Input to Piece. Normal planned work follows Input to Idea to Piece. Format transformation creates a new lineage-linked Piece; platform adaptation creates a Version.

### Context and Production

Assemble the smallest relevant Context Pack with exact Brand, Strategy, Channel, Recipe and CKB revisions. Approve a tool-independent Production Spec before starting a Job. A Job names executor, inputs, outputs, state, attempts and resume boundary. Review is a gate and {{user_name}} approves publishable Versions.

### Publish

Prepare tracking placements before publishing where the channel supports them. Direct publishing remains off by default. Register each real upload as one Publication; retries reconcile before creating another.

### Analyze and Learn

Provider data becomes normalized Evidence with `complete`, `partial`, `unavailable` or `failed` collection state. Evidence supports Observation, then Hypothesis, then at most one scoped Candidate. Approval updates exactly one canonical owner. CKB-targeted learning enters Knowledge Candidate curation.

### Failure and Resume

Every operation returns created/updated refs, changed files, external effects, warnings, errors and a resumable next step. Partial success is retained. Failed siblings do not erase successful platform work. External outcome uncertainty uses `outcome-unknown` and reconciliation.

### Timeline

- **2026-08-02** - Defined the end-to-end v1 workflow and failure boundaries.

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
