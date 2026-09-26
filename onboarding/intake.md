# Fragen, die zu deinem Leben passen

Diese Hilfe ist ein Werkzeug für den Agenten, kein Fragebogen, den jeder vollständig ausfüllen muss. Beginne mit dem ersten Nutzen. Stelle üblicherweise eine bis drei zusammenhängende Fragen; fasse Antworten kurz zusammen. Bekannte Antworten übernehmen, Unklares gezielt nachfragen, nicht jeden Vorschlag bestätigen lassen.

## Regeln für das Gespräch

- „Weiß ich noch nicht“, „später“ und „überspringen“ sind gültige Antworten. Keine Persönlichkeit oder Lebensziele aus fehlenden Antworten ableiten.
- Ein Name oder Pseudonym genügt. Rechtlicher Name, Geburtsdatum und vollständige Lebensgeschichte sind nicht Voraussetzung.
- Die Person kann Antworten tippen oder bereits transkribierten Text aus eigener Spracheingabe bereitstellen. Keine Aufnahme, Transkription, externe Analyse oder Account-Verbindung automatisch starten.
- Bestehende Notizen nur lesen, wenn die Person sie dafür bereitstellt oder den Zugriff beauftragt. Übernommene Aussagen mit Quelle und Datum kennzeichnen; Vermutungen und veralteten Kontext vor Übernahme klären.
- Gib bei Entscheidungen eine Empfehlung und eine verständliche Alternative mit Folgen. Erkläre unbekannte Begriffe kurz. Die Struktur darf später wachsen.
- Finanzielle, gesundheitliche, rechtliche und fremde personenbezogene Details nur bei tatsächlichem Bedarf und im gewünschten Umfang aufnehmen.

## Minimaler Start

1. **Ziel:** „Bei welcher konkreten Sache soll dir dein PersonalOS als Erstes helfen?“ Bei Unklarheit zwei Beispiele anbieten, etwa einen Projektkontext wiederfinden oder einen nächsten Schritt verlässlich festhalten.
2. **Person:** „Wie soll dich dein Agent nennen und was sollte er über deine aktuelle Rolle wissen?“ Pseudonym ausdrücklich zulassen.
3. **Zusammenarbeit:** „Was soll dein Agent immer beachten, und was soll er ohne Rückfrage erledigen dürfen?“ Eine konkrete Formulierung vorschlagen, wenn die Person keine Idee hat; sie nicht als bekannte Präferenz speichern.

Für einen ersten Aufbau reicht das zusammen mit dem geklärten privaten Ziel und technischen Voraussetzungen. Offene Textfelder erhalten **„Noch nicht geklärt“**, keine generischen positiven Charaktereigenschaften.

## Bedarfsgerecht vertiefen

| Thema | Mögliche Frage | Wofür die Antwort gebraucht wird |
| --- | --- | --- |
| Gegenwart und Richtung | Was beschäftigt dich gerade; was möchtest du in den nächsten Wochen verändern? | Bestätigter Kurzkontext und gegebenenfalls später eine Identity-Facette. |
| Arbeiten und Entscheiden | Hilft dir eher ein Vorschlag, ein Vergleich oder gemeinsames Nachdenken? Wie ausführlich soll dein Agent werden? | `USER.md` als kompakter Einstieg; ausführliche Identitätswahrheit bei ihrem Owner. |
| Werte und Grenzen | Was darf ein Agent in deiner Zusammenarbeit nie übergehen? | Eigene bestätigte Regeln; keine automatisch zugeschriebenen Werte. |
| Konkrete Vorhaben | Welches zugesagte Vorhaben hat ein Ergebnis, und was ist der nächste Schritt? | Echte Projects und Actions nach registrierten Templates; Ideen und Daueraufgaben nicht zwanghaft zu Projects machen. |
| Menschen und Organisationen | Welche Beziehung ist für diesen ersten Ablauf wirklich wichtig? | Nur erforderliche Personen-/Organisationskontexte mit belegter Rolle. |
| Vorhandenes System | Wo findest du heute Aufgaben, Notizen, Termine und Entscheidungen? Was funktioniert schon? | Bestehende Owner respektieren und Doppelpflege vermeiden. |
| Quellen und Werkzeuge | Welche konkrete Quelle soll zuerst berücksichtigt werden? Reicht eine einzelne bereitgestellte Notiz? | Kleiner Importumfang; nicht sofort den gesamten Mail- oder Dateibestand anbinden. |
| Routinen | Wann würdest du kurz nachsehen, was offen ist? | Ein realistischer Rhythmus, zunächst ohne Automation. |

## Module verständlich auswählen

Nutze die IDs aus `modules/catalog.json` und die [Modulübersicht](../docs/modules.md); lies das betreffende README bei Bedarf. Stelle keine komplette technische Einkaufsliste vor den ersten Nutzen.

- **Business, Content, Finanzen, Gesundheit:** Nur ergänzen, wenn die Person dort jetzt Kontext führen möchte. Der Kern genügt bereits für Projekte, Aufgaben, Beziehungen und Wissen.
- **Obsidian, Codex, Claude Code:** Passende Hinweise für vorhandene Werkzeuge. Die Auswahl installiert oder bezahlt keine Anwendung und verbindet keinen Account.
- **Externe Signale und Automationen:** Erst nach einem funktionierenden manuellen Ablauf. Kläre Quelle, Befugnis, Aufbewahrung und externe Wirkung einzeln.
- **Hermes, mehrere Agenten/Hosts, Git-Sicherung:** Für einen konkreten Betriebsbedarf. Lokaler Start bleibt möglich. Synchronisation und unabhängige Sicherung getrennt planen.

Beim vollständigen Aufbau sind alle öffentlichen Module enthalten. Die Frage lautet dann, welche davon jetzt eingerichtet werden sollen; nicht jedes Modul muss sofort betrieben werden.

## Antworten in Installationswerte überführen

Kopiere `onboarding/install-values.template.json` an den vereinbarten privaten Ort, nicht neben echte Antworten in das öffentliche Repository. Alle Werte sind Strings. Zeige der Person die kurze Zusammenfassung der eigenen Aussagen und übernimm nur bestätigten Kontext.

`user_name` ist der bestätigte Anzeigename oder ein Pseudonym. `user_slug` ist dessen technischer Name aus Kleinbuchstaben, Zahlen und Bindestrichen, beispielsweise `mein-pos`; er muss keine Identität offenlegen. `user_last_name` darf unbekannt bleiben. Die weiteren `user_*`-Felder enthalten bestätigte Antworten oder „Noch nicht geklärt“. Die neutrale Vorlage ist kein fertig personalisiertes Profil.

`organization_name` und `organization_slug` nur ergänzen, wenn eine Organisation relevant und bestätigt ist; ohne Werte verwendet der Installer eine ausdrücklich unbesetzte Organisationsangabe. Keine fiktive Firma übernehmen. Eine Modulwahl oder ein erwähnter Name ist kein Auftrag, persönliche Records zu erfinden.
