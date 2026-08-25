---
schema_version: pos-v1
id: "{{id_framework_glossary}}"
type: framework
title: "Begriffe einfach erklärt"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Begriffe einfach erklärt

## Purpose

Dieses Glossar übersetzt interne und technische Begriffe in klare Alltagssprache. Agenten sollen die verständliche Formulierung verwenden und den Fachbegriff nur ergänzen, wenn er bei Suche, Code oder Dokumentation hilft.

## Model

Ein Begriff braucht drei Antworten: Was ist das? Wozu dient es? Woran erkennst du es im PersonalOS?

## Components

| Begriff | Einfache Erklärung | Beispiel |
| --- | --- | --- |
| PersonalOS | Ein strukturierter Ordner mit dem Kontext, den du und deine KI-Agenten gemeinsam nutzen. | Projekte, Entscheidungen, Personen und Regeln liegen als lesbare Dateien vor. |
| Kontext | Informationen, die eine Situation verständlich machen. | Ein Agent kennt Ziel, Kunde, letzte Entscheidung und nächsten Schritt. |
| Kontextmanagement | Die Arbeitsweise, mit der du Kontext sammelst, ordnest, aktualisierst und wiederfindest. | Eine Call-Aussage landet beim passenden Projekt und bleibt mit dem Gespräch verknüpft. |
| Owner | Der eine Ort, der eine bestimmte aktuelle Aussage besitzt. | Der aktuelle Projektstatus steht im Projekt, nicht zusätzlich in drei Notizen. |
| Current Truth | Die Aussage, die im Moment gilt. | Das bestätigte Ziel eines Projekts. |
| Working Truth | Ein Arbeitsstand, der noch geprüft oder verändert wird. | Ein Entwurf im Projekt, bevor du ihn als Standard übernimmst. |
| Source Provenance | Die nachvollziehbare Herkunft einer Aussage. Verwende im Gespräch lieber „Quelle und Herkunft“. | Der Projektstand verweist auf den Call, in dem der Kunde ihn bestätigt hat. |
| Evidence | Der Beleg, aus dem du eine Aussage ableitest. | Nachricht, Call-Transkript oder Dokument. |
| Signal | Neuer Input von außen, den du zuerst prüfen musst. | Eine E-Mail enthält eine mögliche neue Deadline. |
| Record | Eine Datei für ein klar bestimmtes Objekt oder Ereignis. | Eine Personendatei oder eine Entscheidung. |
| Profil | Die Regeln für eine Art von Record. | Das Person-Profil legt Pflichtfelder und Ablageort fest. |
| Template | Eine Startvorlage für einen neuen Record. | Die Vorlage für ein neues Projekt. |
| Framework | Ein Denkmodell für wiederkehrende Entscheidungen. | Kontext wird erst Quelle, Reifegrad und Owner zugeordnet. |
| Konvention | Eine gemeinsame Schreib- oder Benennungsweise. | Dateinamen verwenden stabile Slugs. |
| Contract | Eine verbindliche Grenze zwischen Teilen des Systems. Nenne ihn im Alltag „verbindliche Regel“. | Persönliche Daten dürfen beim Boilerplate-Export nicht erscheinen. |
| Runbook | Eine konkrete Anleitung für einen wiederkehrenden Ablauf. | So verbindest du einen zweiten Host. |
| Skill | Ein ausführbarer Arbeitsablauf für einen Agenten. | Ein Call wird analysiert und kontrolliert in das System übertragen. |
| Modul | Ein optionaler Bereich oder eine Fähigkeit, die den Kern ergänzt. | Content, Hermes oder Backup und Git. |
| Host | Der Rechner oder Server, auf dem ein Agent oder Dienst läuft. | Laptop, Desktop oder VPS. |
| Runtime | Die laufende Umgebung eines Agenten oder Programms. | Codex, Claude Code oder Hermes. |
| Adapter | Eine werkzeugspezifische Verbindung zum gleichen Fundament. | Obsidian zeigt die Dateien; Codex bearbeitet sie. |
| External Signal | Ein Signal aus einem fremden System. Verwende im Alltag „externer Input“. | E-Mail, WhatsApp-Nachricht oder Call. |
| Mutation | Eine kontrollierte Änderung an Dateien. Verwende im Alltag „Änderung“. | Ein Agent aktualisiert den bestätigten Projektstatus. |
| Propagation | Das kontrollierte Weitergeben einer bestätigten Änderung an betroffene Bereiche. Verwende im Alltag „Folgeänderungen“. | Eine Entscheidung aktualisiert Projekt und nächste Action, ohne den Text zu duplizieren. |

## Decision Logic

1. Verwende die deutsche Alltagserklärung.
2. Ergänze den Fachbegriff in Klammern, wenn der Nutzer ihn für Suche oder Technik braucht.
3. Erkläre einen neuen Begriff direkt am ersten konkreten Beispiel.
4. Ergänze das Glossar, wenn ein Begriff wiederholt für Verwirrung sorgt.

## Interfaces

- [[system/index]] verlinkt dieses Glossar als sprachlichen Einstieg.
- Regeln, Frameworks, Skills und öffentliche Dokumentation verwenden dieselben Erklärungen.
- Das Glossar ändert keine technische Feldbezeichnung. Es erklärt sie.

## Change History

- **{{install_date}}** | Glossar aus der Boilerplate angelegt.
