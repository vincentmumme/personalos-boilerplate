---
schema_version: pos-v1
id: 019ffc1a-c4f9-74cf-a485-2e59ca85be6b
type: contract
title: "Finance System Boundary"
created: 2026-08-13
updated: 2026-08-23
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.4.0
---

# Finance System Boundary

## Contract

`finance/` besitzt den für {{user_name}} und seine Agenten dauerhaft relevanten Finanzkontext und offene operative Finance-Wahrheit. Das jeweilige Buchhaltungs-, Banking-, Billing- oder externe Fachsystem bleibt Owner seiner Transaktionen und rechtlichen Buchungswahrheit; PersonalOS hält keine unmarkierte Parallelbuchhaltung.

## Scope

Der Vertrag gilt für persönliche und geschäftliche Finance-Records, Belege, wiederkehrende Ausgaben, offene Rechnungen, abrechenbare Stunden, Kostenallokation, Steuerkontext und Verbindungen zu Lexware oder späteren externen Systemen.

## Invariants

- Lexware ist für die heute dort geführte Buchhaltung der externe Source of Truth.
- PersonalOS hält nur agentisch relevanten Kontext, offene Arbeit, Entscheidungen, Pointer und belegte Zusammenfassungen.
- Ein Beleg oder eine Rechnung ist nicht zugleich Task; eine Action entsteht nur bei erfüllter Commitment-Schwelle.
- Gewöhnliche Eingangsbelege und Abo-Rechnungen werden laufend im zuständigen Finance-Owner gesammelt, aber nicht einzeln zur täglichen Operations-Arbeit eskaliert. {{user_name}} bucht sie in einem gemeinsamen Buchhaltungsblock innerhalb der letzten fünf Kalendertage des Monats. Vorher entsteht weder ein täglicher Reminder noch eine eigenständige Ready-Action; ein vorhandener Monatsbatch bleibt bis zum Fenster `deferred`.
- Von dieser Monatsbatch-Regel ausgenommen sind echte Zahlungsfristen, Mahnungen, drohende Sperren, Cashflow-/Rechtsrisiken, strittige Leistungs- oder Steuerfälle und notwendige Zahlungsentscheidungen. Diese werden mit ihrem realen Sachverhalt und ohne erfundene Dringlichkeit separat geroutet.
- Bezahlt, gebucht, storniert und überfällig sind verschiedene fachliche Zustände und werden nicht über ein generisches `status` vermischt.
- Verifizierte Bankkennungen wie IBAN, BIC und Kontonummer dürfen im zuständigen Finance-Account-Record stehen, wenn sie für Zahlung, Abgleich oder Agentenarbeit gebraucht werden.
- Autorisierungs- und Zugangsgeheimnisse bleiben außerhalb des Vaults. Dazu zählen insbesondere vollständige Kartenkennungen, CVV/CVC, PIN, Passwörter, Tokens, Wiederherstellungscodes und Online-Banking-Zugangsdaten.
- Finance-Assets folgen [[system/contracts/core/file-and-asset-boundary]].
- Company-, Project- und Personenkontext wird verlinkt und nicht in Finance dupliziert.
- Jede wiederkehrende Verpflichtung hält in ihrem `Evidence`-Abschnitt genau ein strukturiertes `Receipt Retrieval`-Profil: Belegquelle, Billing-Account ohne Geheimnisse, Portal und Navigationsweg, E-Mail-Suchmuster, erwarteter Belegzeitpunkt, erforderlicher Zahlungsnachweis, Automatisierungsgrad, Auth-Abhängigkeit, Ablageziel, Buchungs-/Steuerbesonderheiten und letzter verifizierter Zugriff. Unbekannte Werte werden als echte Lücke markiert und nicht geraten.
- Ein einzelner Expense-Record hält dagegen nur sein konkretes `Receipt Package`: Originalbeleg, tatsächlicher Abrufweg, Zahlungsnachweis, externer Buchungspointer und gegebenenfalls den Link zum Recurring-Owner. Stabile Providerlogik wird nicht in jeden Monatsbeleg dupliziert.
- Zugangsgeheimnisse bleiben auch im Retrieval-Profil verboten. Zulässig sind sichere Account-Identifier, Portalpfade, Suchmuster und die Aussage, dass ein Passwortmanager, Authenticator oder {{user_name}}-interaktiver Schritt benötigt wird.

## Interfaces

Der SKILL-Workflow führt externe Finance-Aktionen innerhalb seiner Approval-Grenze aus. Operations hält atomare Actions und Attention Trigger. Project- oder Businessowner halten kommerzielle Current Truth; Finance hält den Finanzzustand beziehungsweise den Pointer zum externen Owner.

## Object Model

Der reale Bestand begründet ausschließlich diese Zielklassen. Ihr atomarer Writer-, Sicherheits- und Bestands-Cutover ist abgeschlossen; die Profile sind im schreibbaren Registry-State `pilot` zugelassen:

| Klasse | Primary Profile | Ownergrenze |
|---|---|---|
| Account Context | `finance-account` | Zweck-, Scope-, Nutzungs- und verifizierter Bankkennungskontext; keine Autorisierungs- oder Zugangswerte |
| Payment Source Registry | `finance-payment-source-registry` | kanonische sichere Labels für Konten, Karten und PayPal |
| Expense | `finance-expense` | Eingangsbeleg, Buchungs- und Zahlungszustand ohne Parallelbuchhaltung |
| Client Cost | `finance-client-cost` | Weiterbelastungszustand einer realen Kundenkostenposition |
| Time Entry | `finance-time-entry` | erbrachte Zeit/Leistung und ihr Billing State |
| Invoice | `finance-invoice` | agentisch relevante Projektion einer extern geführten Ausgangsrechnung |
| Recurring Obligation | `finance-recurring-obligation` | stabile Verpflichtung, Fälligkeit, Zuordnung und letzter Buchungsstand |
| Tax Dossier | `finance-tax-dossier` | Current Truth eines Steuerjahres |
| Tax Manifest | `finance-tax-manifest` | Quellen- und Integritätsmanifest des Dossiers |

Navigation verwendet `owner-index`. Budget, freie Transaction-Spiegel oder allgemeine Finance Reports sind nicht vorsorglich zugelassen.

## Compliance

Jeder Finance-Write benennt Source, externe Authority, betroffene Entität und nächsten Zustand. Breite Imports oder Buchungsänderungen benötigen einen repräsentativen Testfall und einen nachvollziehbaren Run-/Recovery-Beleg. Das aktive Finance-Profilpaket setzt diesen Vertrag um. Neue Finance-Klassen oder externe Writer benötigen weiterhin ein vollständiges Admission-, Consumer-, Sicherheits- und Migrationspaket, bevor sie produktiv schreiben dürfen.

## Evolution

Neue externe Finance-Systeme werden als Truth System oder Integration registriert. Neue Recordtypen benötigen eine fachliche State Machine und dürfen nicht nur ein Providerformat spiegeln.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
