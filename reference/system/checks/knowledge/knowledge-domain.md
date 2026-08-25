---
schema_version: pos-v1
id: 01a00173-0000-7000-8000-000000000001
type: check
title: "Knowledge Domain Check"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
check_kind: relation
verifies_refs: ["[[system/contracts/knowledge/topic-wiki-boundary]]"]
---

# Knowledge Domain Check

## Purpose

Prüft, dass Knowledge Records ihrem Profil, ihrem Topic-Owner, ihrer Source-Kette und der Trennung von operativer Wahrheit entsprechen.

## Assertions

- geänderte Knowledge Markdown Records
- registrierte Knowledge Profile und Templates
- Topic Records, abgeleitete Indexe und `wikis.json`
- fremddomainige ContentOS Candidates als ausdrücklich ausgeschlossene Ownerklasse

## Implementation

1. `pos-verify` für die explizit geänderten Records ausführen.
2. Topic-Owner und Pfade vollständig auflösen.
3. Source- und Article-Referenzen mit voller Relationsauflösung prüfen.
4. Indexe und `wikis.json` aus Topic Records neu ableiten und auf Drift prüfen.
5. ContentOS-Candidates weder als Knowledge Records validieren noch durch Knowledge Writer verändern.
6. Bei einem breiten Cutover Source-/Target-Hashes, Consumer-Rewrites und Recovery vor Apply prüfen.

## Invocation

Die portable Basisprüfung führt `python3 system/data-model/scripts/pos_v1.py --root . check-registry` aus. Geänderte Knowledge Records werden zusätzlich mit `pos_v1.py validate --files` und vollständiger Relationsauflösung geprüft.

## Outcomes

- alle Knowledge Records sind gültig und eindeutig einem Topic zugeordnet
- Sources sind unveränderlich und Articles quellengebunden oder ausdrücklich ohne deklarierte Source-Relation
- kein archiviertes Topic lebt unter `.archive`
- kein `_index.md` bleibt als zweiter Index zurück
- generierte Registry und Indexe widersprechen keinem Topic Record
- ContentOS-Fremdowner bleiben unverändert

Bei Erfolg sind Registry, Topic-Owner, Source-Ketten und die Fremdownergrenze grün. Bei einem Fehler stoppen Writes; keine Teilmigration oder automatische Topic-Neuanlage durchführen, sondern den exakten Owner-, Pfad-, Source- oder Consumer-Konflikt beheben und den vollständigen Check wiederholen.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
