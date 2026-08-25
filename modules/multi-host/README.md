# Modul: Mehrere Rechner und Hosts

Ein PersonalOS kann von Laptop, Desktop, Server oder VPS genutzt werden, solange Synchronisation und Zuständigkeiten klar bleiben.

## So nutze ich es

Alle Hosts greifen auf dieselbe logische Wahrheit zu. Pro PersonalOS-Repository gibt es genau einen automatischen Git-Writer. Andere Hosts beginnen lesend oder erhalten den Arbeitsbestand über einen getrennten Dateitransport. Sie führen keinen zweiten automatischen Commit- oder Push-Prozess aus.

## So kannst du es ausprobieren

Synchronisiere zuerst eine reine Testkopie zwischen zwei lokalen Ordnern. Bestimme einen Writer, prüfe Konflikte, Offline-Verhalten und Wiederherstellung und teste danach einen kontrollierten Writer-Wechsel.

## Grenzen

Kein Gerät, Server, Netzwerkpfad oder Synchronisationsdienst wird vorausgesetzt. Ein neuer Writer darf erst starten, nachdem der bisherige automatische Writer gestoppt und der gemeinsame Stand geprüft wurde.
