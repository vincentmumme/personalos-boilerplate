# Deine erste Woche mit PersonalOS

Der erste Erfolg ist ein eigener Kontext, den dein Agent im nächsten Gespräch wiederfindet. Du brauchst dafür nicht sofort alle Lebensbereiche, Konten oder Automationen. Nutze in der ersten Woche einen überschaubaren echten Anwendungsfall.

## Beim ersten Start

Öffne dein **persönliches Zielsystem**, nicht die öffentliche Boilerplate, als Arbeitsordner. Bitte deinen Agenten, zuerst `AGENTS.md` und den dort beschriebenen Kontext zu lesen.

```text
Hilf mir bei [meinem aktuellen Anliegen]. Lies die vorhandenen Quellen, bevor du nachfragst. Zeige, welche Datei die aktuelle Wahrheit besitzt, und halte einen konkreten nächsten Schritt fest. Erfinde keine fehlenden Termine oder Zusagen.
```

Kontrolliere anschließend die wenigen veränderten Dateien. Eine Aufgabe beschreibt die nächste Handlung; ein Project beschreibt ein wirklich gewolltes Vorhaben und sein Ergebnis. Nicht jede Idee benötigt ein Project. Dein Agent wählt die bereits registrierten Profile und Templates.

Falsche Angaben korrigierst du direkt im Gespräch:

```text
Die Angabe [X] stimmt nicht. Richtig ist [Y]. Korrigiere den zuständigen Kontext und die davon betroffenen Verweise. Zeige mir danach die Änderung und die Prüfung.
```

## Am nächsten Tag: Wiederfinden

Starte einen neuen Chat im selben persönlichen Ordner und frage nach dem gespeicherten Anliegen. Bitte um die Quelldatei und den nächsten Schritt. Gelingt das ohne erneut erzählten Kontext, funktioniert die Übergabe. Andernfalls findet ihr heraus, ob der Agent den richtigen Ordner geöffnet, den Einstieg gelesen und die Information an der richtigen Stelle gespeichert hat.

Halte Eingänge klein: eine bereitgestellte Notiz, ein Gesprächsausschnitt oder eine Aufgabe. Lass bestätigte Aussagen von offenen Fragen und Vorschlägen trennen. Du musst nicht sofort deinen gesamten E-Mail- oder Dateibestand importieren.

## Nach einigen Tagen: Rhythmus finden

Ein kurzer täglicher Blick genügt zunächst: Was ist neu, was hat sich geändert und was ist der nächste sinnvolle Schritt? Nach einer Woche prüfst du mit deinem Agenten, was tatsächlich geholfen hat, welche Angaben veraltet sind und welche Struktur unnötig war.

Nur wenn sich ein klarer Bedarf wiederholt, ergänzt ihr ein Modul oder einen Ablauf. Die [Modulübersicht](modules.md) zeigt Voraussetzungen und Grenzen. Automationen kommen nach einem funktionierenden manuellen Ablauf und einer geklärten externen Wirkung.

## Sichern und Wiederherstellung ausprobieren

Richte früh eine zu deinen Geräten passende Sicherung ein. Sie muss frühere Stände wiederherstellen können und unabhängig vom laufenden Arbeitsordner sein. Eine zweite Kopie auf demselben Laufwerk hilft beim Zurücknehmen einer Änderung, schützt aber nicht vor dessen Ausfall. Synchronisation kann versehentliche Löschungen weitertragen.

1. Wähle ein privates Sicherungsziel, etwa ein separates Laufwerk oder einen passend geschützten Backup-Dienst mit Versionen. Sichere den vollständigen persönlichen Ordner einschließlich benötigter versteckter Dateien. Externe große Dateien und Zugangsdaten brauchen ihren eigenen geeigneten Sicherungsweg.
2. Prüfe einmal eine Wiederherstellung in **einen neuen separaten Testordner**. Öffne dort `AGENTS.md`, `USER.md` und einen echten Kontextrecord. Lass den Agenten Links und betroffene Records mit dem Datenmodell-Werkzeug prüfen; nutze eine dafür vorbereitete Python-Umgebung.
3. Halte privat fest, welcher Stand von welchem Sicherungsziel erfolgreich wiederhergestellt wurde. Ein laufender Backup-Job oder das Vorhandensein einer Datei beweist diese Prüfung noch nicht.

Soll später der aktive Arbeitsstand ersetzt werden, stoppe zuerst schreibende Agenten und Automationen, sichere auch den aktuellen Stand und kläre die Wiederanlaufreihenfolge. Stelle nicht ungeprüft direkt über ein aktives System wieder her.

Falls du Git verwenden möchtest, halte das persönliche Repository privat und schließe Secrets aus. Git ist eine mögliche Ebene, kein Ersatz für die Sicherung unversionierter Dateien. Bei mehreren Geräten gilt genau ein automatischer Git-Writer pro PersonalOS; die Details stehen in [Externe Systeme und Synchronisation](external-systems-and-sync.md).

## Später erweitern oder aktualisieren

Deine personalisierte Instanz entwickelt sich eigenständig. Lade eine neuere Boilerplate in einen separaten Quellordner. Vergleiche die gewünschte Änderung samt Abhängigkeiten mit deinem System und sichere den betroffenen Stand vor der Übernahme. Nutze den Weg „Bestehendes verbessern“ aus dem [Onboarding](../onboarding/agent-onboarding.md).

Führe den Installer nicht auf deinem gefüllten persönlichen Ordner aus. Es gibt keinen automatischen Updater, der persönliche Anpassungen zusammenführt. `.personalos-install.json` hilft, den ursprünglichen Stand nachzuvollziehen, und sollte mitgesichert werden. Sie enthält nicht deinen gesamten wiederherstellbaren Kontext.

## Wenn du pausierst

Bitte um einen kurzen Fortsetzungstext mit erledigtem Schritt, offenen Fragen und genau dem nächsten Schritt. Eine Datei dafür gehört an einen vereinbarten privaten Ort. Wenn ein tatsächliches Einrichtungsvorhaben im PersonalOS weiterläuft, verwendet der Agent dessen Project und eine registrierte Working Note. Ein neues Root-Verzeichnis oder ein zweites Persönlichkeitsprofil ist dafür unnötig.

Der folgende Agent liest zuerst den Einstieg und den angegebenen Zwischenstand, prüft den aktuellen Zustand und fragt nur nach fehlenden Informationen.
