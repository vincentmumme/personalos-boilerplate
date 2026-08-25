---
schema_version: pos-v1
id: 019ffb24-1df9-7a24-9b07-e359e32236fd
type: contract
title: "Bootstrap und Portabilität"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# Bootstrap und Portabilität

## Contract

Jede PersonalOS-Instanz besitzt einen kleinen gemeinsamen Root-Bootstrap aus `AGENTS.md`, `INDEX.md`, `USER.md` und `SOUL.md`. Technisch notwendige Agentenadapter wie `CLAUDE.md` verweisen ausschließlich auf `AGENTS.md` und dürfen keine eigenen Regeln, Personas oder Systemkontexte enthalten.

Die Root-Dateien sind konkrete Instanzrecords. Ihre wiederverwendbare Struktur wird getrennt durch registrierte normative Templates besessen; persönliche Werte werden dort ausschließlich über deklarierte Platzhalter oder neutrale Formulierungen eingebunden.

## Scope

Der Vertrag gilt für Root-Einstiege, technische Agentenadapter, ihre vier Primary Profiles, ihre normativen Templates, Fixtures, Renderer, Checks und die spätere Boilerplate-Erzeugung.

Er regelt nicht die konkrete fachliche Wahrheit der verlinkten Domains, die vollständige Identity-Wahrheit, runtimeexterne Agentenanweisungen oder den Distributionsmechanismus einer späteren Boilerplate.

## Invariants

- `AGENTS.md` ist der einzige gemeinsame PersonalOS-Agentenbootstrap.
- `INDEX.md` ist ausschließlich aktive Systemkarte und Navigation.
- `USER.md` ist eine kompakte, owner-verlinkte Projektion auf das menschliche System-Subject und keine zweite Identity Truth.
- `SOUL.md` ist die gemeinsame Grundseele aller PersonalOS-Agenten. Eine registrierte agentenspezifische Persona darf zusätzlich laden, aber gemeinsame Grundbasis und Systemverträge nicht still aufheben.
- `CLAUDE.md` ist ausschließlich ein technischer Pointer auf `AGENTS.md`. Weitere Inhalte sind verboten.
- Systemregeln, Konventionen, Frameworks und Templates besitzen ihre kanonischen Owner unter `system/`; Root-Dateien kopieren sie nicht.
- Ein normatives Root-Template enthält keine persönlichen Daten, Secrets, Projects, Actions, Domainwahrheiten oder runtimespezifischen Sonderregeln einer konkreten Instanz.
- Pflichtplatzhalter sind benannt und müssen vor Materialisierung vollständig aufgelöst sein.
- Die konkrete Instanz darf lesbare Personen- und Instanznamen enthalten. Portabilität wird im Template sichergestellt, nicht durch künstlich generische Instanztexte.
- Die spätere Boilerplate wird aus normativen Templates und generischer Systemstruktur erzeugt, niemals durch blindes Kopieren befüllter persönlicher Root-Dateien.

## Interfaces

```text
technischer Agentenadapter
  -> AGENTS.md
      -> INDEX.md
      -> USER.md
      -> gemeinsame SOUL.md
      -> optionale registrierte agentenspezifische Persona
      -> skills/RESOLVER.md
      -> system/
```

Die vier Primary Profiles besitzen Recordrolle, Foundation, Pfad und Page Shape. Fünf normative Templates besitzen die wiederverwendbaren Blueprints für `AGENTS.md`, `INDEX.md`, `USER.md`, `SOUL.md` und `CLAUDE.md`. Ein semantischer Bootstrap-Check prüft Template-Portabilität, Pflichtpointer, verbotene Adapterinhalte und nicht aufgelöste Platzhalter.

## Compliance

Ein Bootstrap-Paket ist nur zulässig, wenn Registry, Profiles, Templates, neutrale und instanzspezifische Fixtures, Generated Views und semantischer Check gemeinsam grün sind. Der Root-Cutover erfolgt atomar mit den kanonischen Ownern, auf die `USER.md` und andere Bootstrap-Dateien verweisen.

Ein Agentenadapter mit zusätzlichem Regeltext, eine persönliche Angabe in einem portablen Template oder ein nicht aufgelöster Pflichtplatzhalter blockiert die Materialisierung.

## Evolution

Weitere technische Adapter dürfen nur als neue Instanzen desselben engen Pointervertrags entstehen. Zusätzliche gemeinsame Bootstrap-Inhalte werden in `AGENTS.md` oder beim fachlich zuständigen Systemowner ergänzt, nicht in einem Adapter.

Neue Templatevarianten, Sprachen oder agentenspezifische Personas werden additiv über registrierte Profile, Templates und Checks aufgenommen. Sie dürfen die vier Rootrollen nicht still verändern.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
