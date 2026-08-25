---
schema_version: pos-v1
id: 019ffc23-7f24-7463-ab0a-06fda2baadae
type: framework
title: "Research Backend Routing"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Research Backend Routing

## Purpose

Das Framework verhindert, dass Skills dieselbe Research-Aufgabe unterschiedlich klassifizieren oder ohne nachvollziehbare Kosten- und Seiteneffektgrenze ein Backend wählen. Es beschreibt die gemeinsame Auswahl; konkrete Toolaufrufe und Provideradapter bleiben beim ausführenden Skill.

## Model

Jeder Research-Lauf wird zuerst einem Modus zugeordnet. Danach wählt der ausführende Skill anhand verfügbarer Runtime-Fähigkeiten, Kosten und erforderlicher Freigaben ein Backend. Das Ergebnis wird auf ein gemeinsames Minimalkonzept aus Query, Modus, Backend, Runtime, Zeitpunkt, Ergebnissen und Hinweisen normalisiert.

## Components

| Modus | Zweck | Bevorzugte Capability | Freigabe |
|---|---|---|---|
| `general` | allgemeine Web-Recherche | native Websuche oder Exa; Brave als dokumentierter Fallback | nein |
| `discovery` | semantische Quellen-Discovery | Exa | nein |
| `creator` | Creator- und Kanalrecherche | spezialisierter Creator-Extractor | nein |
| `bulk-social` | größere Social-/Profil-Datensätze | geeigneter Actor oder Plattformadapter | bei großen Läufen |
| `trend` | aktuelle Plattform- und Diskussionssignale | zeitnaher Plattformadapter | nein |
| `x-exact` | exakte eigene X-Daten oder Aktionen | authentifizierte X-Capability | bei Schreiben oder Engagement |
| `recent-signal` | Community-Signale eines aktuellen Zeitfensters | Last30Days | bei kostenintensiver Vertiefung |
| `fetch` | konkrete URL lesen | native Fetch- oder Extraktionscapability | nein |
| `crawl` | mehrere Seiten strukturiert extrahieren | Crawl-Capability | bei großem Umfang |
| `browser` | Login-, UI- oder Profilkontext | freigegebene Browser-Capability | bei externen Aktionen |
| `deep` | mehrstufiger kostenintensiver Report | Deep-Research-Capability | immer pro Aufruf |

Benötigte Credential-Namen und ihre vorhandenen Runtime-Surfaces werden in `system/access/` und `system/observability/` gepflegt. Dieses Framework besitzt weder Secret-Werte noch eine zweite Access-Wahrheit.

## Decision Logic

1. Der Skill bestimmt den kleinsten passenden Modus; `general` oder `fetch` sind die Defaults.
2. Native Runtime-Capabilities werden bevorzugt, wenn sie die Aufgabe vollständig und ohne zusätzliche Seiteneffekte erfüllen.
3. Fehlt ein erforderliches Backend oder Credential, stoppt der Lauf mit benannter Lücke; ein Wechsel zu einem semantisch anderen Backend geschieht nicht still.
4. Ein Fallback wird im Ergebnis mit Backend und Grund dokumentiert.
5. `deep` wird nie automatisch gewählt und benötigt für jeden Aufruf eine explizite Bestätigung.
6. Schreiben, Engagement, Versand, Veröffentlichung und andere externe Wirkungen benötigen die Freigabe des owning Skills unabhängig vom Research-Modus.
7. Neue Backends erweitern eine bestehende Capability zuerst; sie erzeugen nur dann einen neuen Modus, wenn sich die fachliche Aufgabe unterscheidet.

## Interfaces

Konsumierende Skills referenzieren dieses Framework direkt über `pos_system_refs`, sofern sie die gemeinsame Auswahl wirklich verwenden. Provideradapter, API-Payloads, lokale Prompts und Retry-Logik bleiben skilllokale Implementierung. Ein normalisiertes Ergebnis enthält mindestens:

```yaml
query: "…"
mode: general|discovery|creator|bulk-social|trend|x-exact|recent-signal|fetch|crawl|browser|deep
backend: "…"
runtime: "…"
timestamp: "<ISO-8601 mit Offset>"
results: []
notes: "…"
```

Das Storage-Shape eines persistierten POS-Records wird weiterhin ausschließlich durch sein registriertes Profile und Systemtemplate bestimmt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
