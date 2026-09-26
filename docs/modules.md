# Passende Erweiterungen auswählen

Beginne mit dem Ergebnis, das du erreichen möchtest. Dein Agent empfiehlt dazu die kleinste passende Auswahl. Du kannst später bewusst ergänzen. Der Kern enthält bereits Personen, Unternehmen, Projekte, Aufgaben, Entscheidungen, Wissen und Gesprächskontext.

Ein installiertes Modul ergänzt derzeit einen Bereichseinstieg oder eine Anleitung. Eine verbundene Anwendung und ein erfolgreich getesteter Ablauf sind weitere Schritte. Auch die vollständige Installation richtet keine Accounts, Dienste oder Automationen automatisch ein.

## Was du bekommst

| Modul | Sinnvoll für | Gelieferter Inhalt | Zusätzlich nötig / mögliche Kosten | Kleiner Erfolgstest |
|---|---|---|---|---|
| business | Eigene Angebote, Produkte oder Geschäftsmodelle | Bereichseinstieg für Business | Bestätigter eigener Kontext | Ein reales Angebot mit Quelle erfassen und in einem neuen Chat wiederfinden. |
| content | Regelmäßige Inhalte | Bereichseinstieg für Ideen, Stücke und Veröffentlichungen | Eigenes Beispiel; Kanalzugriffe erst bei Bedarf | Eine Idee von einem beauftragten Stück und einer tatsächlichen Veröffentlichung unterscheiden. |
| finance | Finanziellen Kontext organisieren | Bereichseinstieg für Finanzen | Eigene Speicher- und Zugriffsentscheidung; externe Buchhaltung bleibt zuständig | Einen geeigneten Beleg referenzieren, ohne eine Zahlung oder Buchung zu erfinden. |
| health | Persönliche Gesundheits- oder Trainingsinformationen | Bereichseinstieg für Gesundheitskontext | Bewusste Auswahl geeigneter Daten; Anbindungen optional | Einen Messwert mit Quelle und Datum von einer eigenen Einschätzung unterscheiden. |
| obsidian | Dateien visuell lesen und verlinken | Anleitung zum Öffnen des POS | Obsidian optional; Zusatzdienste separat prüfen | Dieselbe Datei und ihren Link im Editor und mit dem Agenten öffnen. |
| codex | Mit Codex im eigenen Ordner arbeiten | Anleitung zum Agenteneinstieg | Installierter Zugang, Anmeldung und passende Nutzungsberechtigung | In einem frischen Chat den eigenen Startkontext finden und korrekt verwenden. |
| claude-code | Mit Claude Code im eigenen Ordner arbeiten | Anleitung zum Agenteneinstieg | Installierter Zugang, Anmeldung und passende Nutzungsberechtigung | Den Bootstrap lesen und einen bestätigten kleinen Auftrag im passenden Owner ausführen. |
| hermes | Eine zusätzliche Agentenlaufzeit verwenden | Anleitung zu Rolle, Zugriff und Betrieb | Eigene Installation und Konfiguration; Modell- und gegebenenfalls Hostingkosten | Einen begrenzten manuellen Auftrag ausführen und dessen Ergebnis überprüfen. |
| multi-agent | Mehrere Agenten auf derselben Grundlage verwenden | Anleitung zu Rollen und Zuständigkeiten | Zwei funktionierende Zugänge mit abgestimmten Rechten | Der zweite Agent findet das bestätigte Ergebnis des ersten, ohne Chatverlauf zu kopieren. |
| external-signals | Nachrichten, Texte oder Gesprächsbelege einordnen | Anleitung und Verweis auf lokale Call-Analyse im Kern | Für bereitgestellten Text kein Connector; für Abruf passende Rechte und ggf. Providerkosten | Eine bereitgestellte Quelle nachvollziehbar auswerten; unsichere Aussagen offen lassen. |
| automations | Erprobte Abläufe regelmäßig ausführen | Anleitung für Auslöser, Kontrolle und Fehlerbehandlung | Zuerst funktionierender manueller Ablauf, dann Scheduler und Laufzeit | Einen Testlauf auslösen, Ergebnis und Fehlerpfad erkennen und Ausführung wieder deaktivieren. |
| backup-git | Änderungen nachvollziehen und wiederherstellen | Anleitung zu Versionierung, Sicherung und Rückweg | Git und bewusst gewähltes Sicherungsziel; ggf. Speicherkosten | Eine Testdatei aus der Sicherung in einen separaten Ordner zurückholen und vergleichen. |
| multi-host | Auf mehreren Geräten arbeiten | Anleitung zur Host- und Writer-Aufteilung | Abgestimmter Dateitransport und Zugänge; ggf. Hostingkosten | Eine Teständerung übertragen und genau einen automatischen Git-Writer nachweisen. |

Die auswählbaren IDs stehen im [Modulkatalog](../modules/catalog.json). Die allgemeinen Verträge, Datenmodelle und Vorlagen liegen im Kern. Die Module bringen keine persönlichen Daten mit.

## Empfehlung statt Pflichtpaket

- **Erstes eigenes POS:** Kern und der tatsächlich verwendete Agentenzugang. Einen benötigten Fachbereich ergänzen. Sicherung vor der Übergabe klären.
- **Vorhandenes POS verbessern:** Zuerst ein konkretes Problem und passende Bestandteile bestimmen. Siehe [Onboarding](../onboarding/agent-onboarding.md).
- **Vollständige Grundlage:** Alle Module liefern die gesamte portable Struktur. Jeder externe Dienst wird trotzdem einzeln eingerichtet und geprüft.

Für jede ausgewählte Anbindung hält der Agent fest: Zweck, Datenfluss, benötigte Rechte, Kostenart, verantwortlicher Account, erfolgreicher Test und wie du den Zugriff wieder entziehst. Zugangsdaten gehören in den dafür vorgesehenen Zugangsspeicher, niemals in diese Dokumentation oder in einen öffentlichen Issue.

## Später erweitern oder zurücknehmen

Der Installer baut neue leere Zielordner. Er ist kein Modul-Updater für dein befülltes System. Zusätzliche Module werden zunächst in einer getrennten Vergleichsinstallation betrachtet und nach Sicherung sowie Abgleich ihrer Abhängigkeiten übernommen.

Zum Rückbau zuerst Automationen stoppen beziehungsweise Zugriffe widerrufen, dann abhängige Inhalte und Links prüfen. Eigene Records nicht löschen, nur weil das zugehörige Modul nicht mehr benötigt wird. Behalte die Sicherung bis zur erfolgreichen Prüfung des neuen Zustands.
