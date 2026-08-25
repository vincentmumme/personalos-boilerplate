---
schema_version: "pos-v1"
id: "01a002b7-e000-70ea-bd3e-680123ca8a03"
type: "contract"
title: "ContentOS v1 Analytics Adapter Contract"
created: "2026-08-02"
updated: "2026-08-02"
lifecycle: "active"
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: "1.0.0"
---

# ContentOS v1 Analytics Adapter Contract

## Contract

### Normalized Result

Every pull returns provider, account, capability, observed interval, provider timestamp and timezone, collected time, adapter version, provenance reference, and one state: `complete`, `partial`, `unavailable`, or `failed`.

`unavailable` is never normalized to zero. A partial platform failure cannot erase successful sibling results.

### Data Boundary

Markdown may contain approved aggregate metrics, qualitative Evidence, attribution class, confidence, and interpretation. Raw events, user IDs, emails, IP addresses, raw ManyChat profiles, tokens, and cross-system identity graphs remain outside Git.

### Provider Boundary

Adapters declare authentication key names, capabilities, pagination, rate limits, retention metadata, and error semantics. Secrets use the PersonalOS environment loader and never enter records, fixtures, logs, or errors.

### Retry

Read retries use the same snapshot identity. External write timeouts return `outcome-unknown` and require remote reconciliation before retry.

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
