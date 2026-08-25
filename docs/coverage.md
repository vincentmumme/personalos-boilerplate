# Abdeckung und aktueller Reifegrad

## Was heute abgedeckt ist

Der aktuelle Kern wird aus dem versionierten Stand des privaten PersonalOS gebaut und enthält:

- Root-Bootstrap und Systemkarte,
- generische USER-, SOUL- und Identity-Grundrecords,
- alle bewusst übernommenen Systemverträge,
- Konventionen, Frameworks, Prinzipien und Regeln,
- das aktive Datenmodell mit Profilen, Modulen, Schemas und generischen Laufzeithelfern,
- kanonische Record-Templates,
- portable Systemchecks,
- Core-Runbooks für sichere Mutationen,
- die Kernfähigkeiten `pos-verify`, `task-manager`, `priority-dashboard`, `log`, `skillify`, `write-skill` und die datenschutzbewusste lokale Call-Analyse `analyse-call`,
- die elf allgemeinen Root-Bereiche mit verständlichen Einstiegen,
- ein Glossar für interne und technische Begriffe.

Der Build ergänzt optionale Module für Business, Content, Finanzen, Gesundheit, Obsidian, Codex, Claude Code, Hermes, mehrere Agenten, externe Signale, Automationen, Backup und Git und mehrere Hosts.

## Was bewusst nicht roh übernommen wird

- persönliche und geschäftliche Daten,
- Interaktionen, Calls, E-Mails, Chats und äußere Signale,
- Actions, Projects, Decisions, Daily-, Health-, Finance-, Content- und Knowledge-Records,
- aktive Automationen und ihre Ausgaben,
- Hosts, Runtimes, Services, Zugriffe und Observability-Zustand,
- Migrationshistorie und Regressionstests der privaten Instanz,
- private Obsidian-, Claude-Code- und Skill-Lock-Konfiguration,
- Fach-Skills mit privaten Beispielen, Kundenlogik oder Runtime-Annahmen.

Diese Dateien gelten nicht als vergessen. Die Export-Policy klassifiziert sie weiterhin. Öffentliche Module beschreiben die wiederverwendbare Architektur und sichere Einstiege. Sie kopieren keine privaten Laufzeitkonfigurationen und versprechen keine funktionale Parität zu Vincents konkreten Rechnern, Accounts oder Automationen.

## Bedeutung von 100 Prozent

Die Referenzinstanz muss vollständig inventarisiert sein. Jede versionierte Datei muss eine explizite Behandlung besitzen. Der Build bricht bei einer neuen unklassifizierten Datei ab.

Vollständige Abdeckung bedeutet nicht, dass jede private Datei im öffentlichen Repository landet. Sie bedeutet, dass nichts still ignoriert wird und keine wiederverwendbare Systemlogik unbemerkt verloren geht.

## Aktuelle Release-Grenze

Version 0.1.0 enthält Kern, Module, vollständige öffentliche Referenz, agentengeführtes Onboarding, Release-Prüfungen und MIT-Lizenz. Die technische Freigabe wird über Tests, Build-Audit, vollständigen Git-History-Secret-Scan und einen isolierten Clean-Install belegt.

Nicht enthalten sind vollständige operative Parität aller privaten Fach-Skills, aktive Connectoren oder ein fertiger Hermes-/VPS-Betrieb. Diese Grenze ist Teil des Produktversprechens und kein stiller Restpunkt.

Vor der öffentlichen Veröffentlichung bleiben das externe GitHub-Freigabegate und die Prüfung des öffentlichen Links ohne Maintainer-Zugriff.

Ein automatischer Updatepfad für bereits personalisierte Nutzerinstanzen gehört nicht zu Version 0.1.0.
