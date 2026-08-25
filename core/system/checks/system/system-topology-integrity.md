---
schema_version: pos-v1
id: 019ffbfe-fa7b-77c4-b0a4-a4b81e1f559d
type: check
title: "System Topology Integrity"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/system/system-topology-and-access]]", "[[system/principles/core/system-truth-is-self-describing]]"]
check_kind: health
verifies_refs: ["[[system/contracts/system/system-topology-and-access]]", "[[system/principles/core/system-truth-is-self-describing]]"]
---

# System Topology Integrity

## Purpose

Prüft, dass alle materialisierten Systemtopologie-Records registrierte Shapes, auflösbare Beziehungen und eine Secret-freie Access-Grenze einhalten.

## Assertions

- Agenten, Persona-Overlays, Runtimes, Hosts, Services, Integrationen, Access, Operating Systems und Views validieren gegen ihr pos-v1-Profil.
- Agent–Runtime–Host–Service-Relations lösen auf und zeigen auf erlaubte Profile.
- Access-Frontmatter enthält keine Secret-, Token-, Password-, API-Key- oder Private-Key-Werte.
- Observability ist als abgeleitete View markiert und erzeugt keine zweite gewünschte Systemwahrheit.

## Implementation

`system/checks/system/system_topology_integrity.py` lädt die zentrale Registry, entdeckt ausschließlich die zugelassenen Systempfade und führt Relations- sowie Secret-Key-Prüfungen aus.

## Invocation

```bash
python3 system/checks/system/system_topology_integrity.py
```

## Outcomes

- `pass`: alle entdeckten Records und Beziehungen sind gültig.
- `fail`: Profil, Relation, Secret-Grenze oder View-Ownership ist verletzt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
