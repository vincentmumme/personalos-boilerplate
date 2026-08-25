---
schema_version: "pos-v1"
id: "01a002b7-e000-7599-8af3-e26e9ed5510d"
type: "contract"
title: "ContentOS v1 Storage Model"
created: "2026-08-02"
updated: "2026-08-21"
lifecycle: "active"
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: "1.1.0"
---

# ContentOS v1 Storage Model

## Contract

### Truth Layers

- Markdown/Git: objects, decisions, manifests, normalized evidence and relationships.
- Active Storage Profile: raw media, projects, graphics, renders and Finals.
- Provider: collaboration, publishing, redirects and high-volume telemetry.
- Backup/archive: recovery, never an active editing truth unless explicitly selected.

### Asset Identity

Assets have stable IDs independent from path/provider. Manifests record `storage_profile_id`, relative path or external URL, role, version, owner, sensitivity, checksum where useful, availability, backup state and related object IDs. One version is canonical/Final.

### Initial Profile

`pos-assets-local` resolves through `POS_ASSET_ROOT` and `asset://content/`. Arbeitsrechner, external SSD and cloud/team profiles remain interchangeable implementations. See storage.

### Telemetry and Collection Data

ContentOS owns the identity and manifest of collected data, not necessarily every raw row. Comments, replies, metric histories and authenticated platform insights may live in a spreadsheet, database, object store or another replaceable backend. Every external dataset remains addressable from ContentOS through a stable dataset or batch identity, Publication relation, provider/source, collection timestamp, covered time range, cursor or completeness state, schema version and storage pointer.

Changing the storage backend must not change Piece, Version, Publication or Evidence identity. Analysis consumes the normalized collection layer and its manifests instead of coupling directly to a platform or storage implementation.

### Timeline

- **2026-08-02** - Established provider-neutral storage and manifest ownership.

## Scope

ContentOS records, workflows, storage, analytics or capability boundaries defined by this contract.

## Invariants

The global POS-v1 registry owns record shape; this contract owns only Content-domain semantics. External spreadsheets and databases may hold high-volume data but never become an untracked second Content graph or replace COS-owned identity, relations and collection coverage.

## Interfaces

Consumed through the ContentOS skill and its deterministic validators.

## Compliance

Changes require registry-safe verification and ContentOS semantic tests.

## Evolution

Revise through the ContentOS migration project and preserve explicit supersession.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
