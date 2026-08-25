# PersonalOS Recording Demo

Dieses Verzeichnis ist die reproduzierbare Quelle für Vincents separates `personalos-demo` Repository.

## Datenschutzgrenze

- Angaben über Vincent und Mummentum dürfen reale, öffentlich verwendbare Eigeninformationen enthalten.
- Andere Personen, Unternehmen, Gespräche, Projekte und Signale sind vollständig erfunden.
- Zugangsdaten, Tokens, Netzwerkadressen, echte Transkripte und private Host-Konfigurationen gehören nicht in das Demo.
- Die Namen `Nordlicht Handel`, `Lena Hoffmann` und `Jonas Becker` bezeichnen ausschließlich das fiktive Demo-Szenario.

## Aufbau

- `values.json` personalisiert den vollständigen Boilerplate-Installer für Vincent.
- `overlay/` ergänzt das installierte System um zusammenhängende, datenmodellkonforme Demo-Records.
- Der `demo`-Befehl installiert alle Module, legt das Overlay darüber und validiert alle ergänzten Markdown-Records vor der Übergabe.

## Build

```bash
pos-boilerplate demo \
  --build . \
  --destination ../personalos-demo-build \
  --values examples/recording-demo/values.json \
  --fixtures examples/recording-demo/overlay
```

Der Build verweigert ein nicht leeres Ziel. Eine bestehende Aufnahmeinstanz wird nie automatisch ersetzt.

## Vorbereiteter Aufnahmeablauf

Der Discovery Call vom 22. August liegt absichtlich nur als Event und Evidence vor. Es existiert noch keine Analysis. In der Aufnahme verarbeitet ein erster Codex-Task diesen Beleg mit `skills/analyse-call/SKILL.md`. Ein zweiter, neuer Task liest danach denselben aktualisierten Projektkontext und erstellt die bestätigte Workshop-Agenda. So bleibt sichtbar, dass der Chatverlauf nicht die Übergabe zwischen Agenten ist.
