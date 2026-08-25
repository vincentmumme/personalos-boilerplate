---
schema_version: pos-v1
id: 019fffaf-27c9-7591-833d-ce93a856c474
type: contract
title: "Health System Boundary"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Health System Boundary

## Contract

`health/` besitzt {{user_name}}s dauerhaft relevanten persönlichen Gesundheits-, Fitness-, Trainings- und Recovery-Kontext. Externe Geräte- und Gesundheitsdienste bleiben Owner ihrer Rohmessungen; PersonalOS hält normalisierte, quellengebundene Health Truth für Verlauf, Reflexion und Entscheidungen, aber keine unmarkierte Kopie eines Providers und keine medizinische Diagnose.

## Scope

Der Vertrag gilt für Health-Profil, WHOOP-Ableitungen, Training, Körperwerte, Health-Dailies, Reviews und spätere Health-Objektklassen. Er gilt nicht für Run Receipts, allgemeine Daily-Aktivität, operative Actions, Secrets, große Exporte oder ärztliche Primärunterlagen ohne explizites Asset- und Datenschutzmodell.

## Invariants

- WHOOP und andere Provider liefern Signale; ihre Rohdaten werden nicht automatisch zur persönlichen Health Truth.
- Normalisierte Tageswerte referenzieren Provider und Zeitpunkt ihrer Quelle.
- `health/` besitzt den fachlichen Zustand. Automation Runs liegen unter `automations/`, allgemeine Tageschronik unter `daily/` und konkrete Commitments unter `operations/`.
- Project-Arbeit kann Health-Struktur, Integrationen oder Programme entwickeln. Erst angenommene Ergebnisse werden in den Health-Owner übertragen.
- Fehlende Daten werden sichtbar markiert; sie werden nicht durch Scheingenauigkeit oder stilles Fortschreiben ersetzt.
- Medizinische Diagnosen, Therapieentscheidungen und akute Risikobewertungen werden nicht autonom aus Wearable-Daten erzeugt.
- Tokens und Provider-Secrets bleiben außerhalb des Vaults. Große Exporte und binäre Befunde folgen [[system/contracts/core/file-and-asset-boundary]].
- Neue Health-Module entstehen aus realer Nutzung und stabiler Semantik, nicht vorsorglich.

## Interfaces

```text
Provider / manuelle Source
  -> Automation oder owning Health Capability
    -> normalisierte Health Evidence
      -> Health Current Truth / Verlauf
        -> optionale Action oder Daily-Referenz
```

`system/` besitzt Integrations-, Runtime- und Access-Metadaten. `projects/` besitzt Migrationen und Weiterentwicklung. `daily/` darf Health-Aktivität referenzieren, aber keine zweite Tages-Health-Wahrheit führen.

## Compliance

Jeder Health-Write benennt Quelle und fachlichen Zeitpunkt, hält Providerzustand und persönliche Ableitung auseinander und durchläuft den zuständigen Health-Check. Ein breites neues Profil oder ein Provider-Cutover benötigt repräsentative Fixtures, Consumerprüfung und Recovery-Grenze.

## Evolution

Das heutige schlanke Health-Modell bleibt zulässig, bis reale Nutzung weitere Profile rechtfertigt. Neue Provider werden als Integration und externe Authority registriert; sie erzeugen keinen neuen Root und keine parallele Health-Datenbank.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
