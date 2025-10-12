# Home Assistant Laufschrift Integration

Diese Integration ermöglicht die Steuerung einer Laufschrift über Home Assistant.

## Funktionen

*   Text einstellen
*   Helligkeit einstellen
*   Geschwindigkeit einstellen
*   Farbe einstellen
*   PC herunterfahren

## Voraussetzungen

*   Home Assistant 2023.1 oder höher
*   HACS (Home Assistant Community Store)

## Installation

1.  Füge dieses Repository als Custom Repository in HACS hinzu.
    *   Repository: `richieam93/homeassistant-laufschrift`
    *   Kategorie: Integration
2.  Installiere die "Laufschrift" Integration über HACS.
3.  Starte Home Assistant neu.

## Konfiguration

1.  Gehe zu "Konfiguration" -> "Integrationen" in Home Assistant.
2.  Klicke auf den "+ Integration hinzufügen" Button und suche nach "Laufschrift".
3.  Gib die IP-Adresse Deiner Laufschrift-App ein.
4.  Konfiguriere die gewünschten Optionen (Helligkeit, Geschwindigkeit, Farbe).

## Verwendung

Nach der Konfiguration werden folgende Entitäten erstellt:

*   `sensor.laufschrift_text`: Zeigt den aktuellen Text an.
*   `sensor.laufschrift_brightness`: Zeigt die aktuelle Helligkeit an.
*   `sensor.laufschrift_speed`: Zeigt die aktuelle Geschwindigkeit an.
*   `select.laufschrift_color`: Ermöglicht die Auswahl der Farbe.
*   `switch.pc_herunterfahren`: Schalter zum Herunterfahren des PCs.

Du kannst diese Entitäten in Deinen Automatisierungen und Skripten verwenden.

## Beispiel Automation

```yaml
alias: Laufschrift aktualisieren
trigger:
  - platform: state
    entity_id: input_text.laufschrift_text
action:
  - service: laufschrift.laufschrift_set_text
    data:
      text: "{{ trigger.to_state.state }}"