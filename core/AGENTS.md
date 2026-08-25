---
schema_version: pos-v1
id: "{{id_agent_entry}}"
type: agent-entry-pointer
title: "PersonalOS Agent Entry"
created: "{{install_date}}"
updated: "{{install_date}}"
entry_kind: common-bootstrap
---

# PersonalOS Agent Entry

Dies ist das persönliche, Markdown-basierte Kontextsystem von {{user_name}}.

## Verbindlicher Start

Lies vor der Arbeit:

1. [[INDEX]] – Systemkarte und kanonische Owner
2. [[USER]] – kompakter Kontext über die Person
3. [[SOUL]] – gemeinsame Verhaltensbasis
4. [[system/index]] – Regeln, Verträge, Datenmodell und Prüfungen
5. [[skills/RESOLVER]] – verfügbare ausführbare Fähigkeiten

## Arbeiten im PersonalOS

- Neue Informationen werden zuerst dem richtigen Owner zugeordnet.
- Neue oder geänderte Records folgen dem registrierten Profil und Template unter [[system/data-model/index]].
- Mutationen folgen [[system/contracts/core/personalos-mutation-contract]] und enden mit der zuständigen Prüfung.
- Neue Root-Ordner, Profile, Felder oder Normen werden nicht improvisiert.
- Agent, Editor und Host sind austauschbare Werkzeuge. Die Dateien bleiben die gemeinsame Wahrheit.

## Autorität

- `/system` besitzt die allgemeine Systemlogik.
- Skills führen konkrete Abläufe aus und besitzen keine konkurrierende Systemverfassung.
- Fachliche Wahrheit liegt bei ihrem Domain- oder Entity-Owner.
- Bei einem echten Konflikt wird der zuständige Owner geprüft oder die Person gefragt.
