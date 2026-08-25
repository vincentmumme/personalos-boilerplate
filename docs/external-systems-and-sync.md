# Externe Systeme und Synchronisation

PersonalOS soll unterschiedliche Werkzeuge und Geräte verbinden, ohne mehrere konkurrierende Wahrheiten zu erzeugen. Dieses Dokument beschreibt das portable Betriebsmodell. Es enthält keine konkreten Hosts, Accounts, Tokens oder privaten Pfade.

## Externe Systeme behalten klare Zuständigkeiten

PersonalOS besitzt persönlichen Kontext, Systemregeln, Navigation, Aufgaben und die ausdrücklich aufgenommenen Lebens- und Arbeitsbereiche. Es muss nicht jeden Rohdatentyp selbst speichern.

Typische externe Owner sind:

- E-Mail- und Chat-Anbieter für ihre Nachrichten,
- Kalender für gebuchte Termine,
- Buchhaltungssysteme für Buchungs- und Belegwahrheit,
- Secret Stores für Passwörter, Tokens und Schlüssel,
- einzelne Repositories für ihren Quellcode,
- Asset-Speicher für große Bilder, Audio- und Videodateien,
- spezialisierte Datensysteme für große oder häufig veränderte Datensätze.

PersonalOS hält dazu nur den nötigen Kontext, einen sicheren Pointer, die relevante Evidenz oder einen bestätigten abgeleiteten Stand. Eine Kopie wird nicht allein deshalb zur neuen Wahrheit, weil ein Agent sie eingelesen hat.

Der allgemeine Quellvertrag steht in [Source Provenance](../core/system/contracts/core/source-provenance.md). Das optionale Modul [Externe Signale](../modules/external-signals/README.md) erklärt den Einstieg für Calls, Nachrichten, Feeds und andere Quellen.

## Keine Secrets im Repository

Passwörter, API-Keys, Tokens, private Schlüssel und vergleichbare Werte gehören in einen dafür vorgesehenen Secret Store oder eine klar dokumentierte lokale Runtime. PersonalOS darf beschreiben, welcher Zugang benötigt wird und wo er sicher verwaltet wird. Der eigentliche Secret-Wert wird nicht in Markdown oder Git dupliziert.

## Ein Git-Writer pro PersonalOS-Repository

Sobald mehrere Geräte beteiligt sind, braucht der Git-Betrieb eine eindeutige Zuständigkeit:

1. Pro PersonalOS-Repository gibt es genau einen automatischen Git-Writer.
2. Nur dieser Host erstellt und pusht automatische PersonalOS-Commits zu GitHub.
3. Andere Hosts dürfen lesen, suchen, indexieren oder über einen getrennten Dateitransport am Arbeitsbestand teilnehmen.
4. Auf anderen Hosts läuft kein zweiter automatischer Commit-, Pull-, Merge- oder Push-Prozess für dasselbe Repository.
5. Konflikte oder Drift stoppen automatische Writes, bis ein kanonischer Stand bestimmt ist.

Der Writer kann ein Mac Mini, ein VPS oder ein anderer zuverlässiger Host sein. Das Gerät ist austauschbar. Entscheidend ist, dass die Verantwortung eindeutig bleibt.

## Git und Dateisynchronisation haben verschiedene Aufgaben

Git hält nachvollziehbare Versionen der freigegebenen Text- und Systemdateien. GitHub kann als privates Remote für Historie und Wiederherstellung dienen.

Ein Dateisynchronisationswerkzeug kann den aktuellen Arbeitsbestand zwischen autorisierten Geräten transportieren. Es ersetzt keine Git-Historie und darf keinen zweiten Git-Writer erzeugen. Große, sensible oder veränderliche Daten können einen eigenen Speicher- und Backupweg erhalten.

Das Modul [Backup und Git](../modules/backup-git/README.md) beschreibt die Versionierungsgrenze. Das Modul [Mehrere Rechner und Hosts](../modules/multi-host/README.md) beschreibt die Hostgrenze.

## Ein sicherer Start mit zwei Geräten

1. Eine reine Testkopie mit fiktiven Daten anlegen.
2. Einen Host als einzigen automatischen Git-Writer festlegen.
3. Den zweiten Host zunächst nur lesend anbinden.
4. Dateitransport, Offline-Verhalten und Konflikterkennung testen.
5. Eine Datei aus Git und einen ausgeschlossenen Datentyp aus dem separaten Backup wiederherstellen.
6. Erst danach automatische Prozesse für den echten Bestand aktivieren.

## Writer-Wechsel und Failover

Ein zweiter Host wird nicht parallel zum neuen Writer. Der Wechsel erfolgt als bewusster Cutover:

1. Alten automatischen Writer stoppen.
2. Letzten erfolgreichen Commit und Remote-Stand prüfen.
3. Offene lokale Änderungen und Dateisynchronisation vollständig abgleichen.
4. Neuen Host auf exakt diesen Stand bringen.
5. Writer-Verantwortung und Recovery-Pfad dokumentieren.
6. Automatische Writes auf dem neuen Host aktivieren.
7. Nachweisen, dass der alte Host nicht mehr automatisch schreibt.

Bei ungeklärtem Drift bleiben beide Automationen aus. Zuerst wird ein kanonischer Stand festgelegt.

## Was ein Agent vor der Einrichtung klärt

- Welcher Host übernimmt die eindeutige Writer-Rolle?
- Welche Dateien dürfen in Git und welche brauchen einen anderen Speicherweg?
- Welches System besitzt die Wahrheit für externe Daten?
- Wo liegen Secret-Werte?
- Wie werden Konflikte erkannt und Writes gestoppt?
- Wie sieht eine getestete Wiederherstellung aus?
- Wie wird ein späterer Writer-Wechsel kontrolliert durchgeführt?

Die Boilerplate richtet keinen Remote, Account, Token, Synchronisationsdienst oder automatischen Push ein. Sie liefert die Regeln und Runbooks, mit denen ein Nutzer und sein Agent diese Infrastruktur bewusst aufbauen können.
