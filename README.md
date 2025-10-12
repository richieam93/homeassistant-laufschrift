# Home Assistant Laufschrift Integration

Diese Integration ermöglicht die Steuerung einer Laufschrift über Home Assistant. Sie ermöglicht das Einstellen von Text, Helligkeit, Geschwindigkeit und Farbe über eine benutzerdefinierte Komponente.

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

1.  **Software auf dem PC starten**:
    *   Vor der Installation der Integration muss die Laufschrift-Software auf dem PC gestartet werden. Diese befindet sich im Ordner `homeassistant-laufschrift\Laufschrift_exe`.
    *   Die Software kann entweder manuell oder über ein Skript gestartet werden.
2.  **Integration hinzufügen**:
    *   Gehe zu "Konfiguration" -> "Integrationen" in Home Assistant.
    *   Klicke auf den "+ Integration hinzufügen" Button und suche nach "Laufschrift".
    *   Gib die IP-Adresse Deines PCs ein, auf dem die Laufschrift-App ausgeführt wird.
    *   Konfiguriere die gewünschten Optionen (Helligkeit, Geschwindigkeit, Farbe).

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
alias: Temperaturen + Tankstelle auf Laufschrift
description: Zeigt stündlich die Temperaturen verschiedener Sensoren auf der Laufschrift an
trigger:
  - platform: time_pattern
    minutes: /50
action:
  - service: laufschrift.laufschrift_set_text
    data:
      text: >-
        Temperaturen: Wohnzimmer: {{ states('sensor.airpurifier_temperature')
        }}°C, Schlafzimmer: {{
        states('sensor.stecker_mucken_device_temperature') }}°C, TV Sideboard:
        {{ states('sensor.stecker_tv_leds_device_temperature') }}°C, Caffè
        Maschine: {{ states('sensor.stecker_kaffe_device_temperature') }}°C,
        Balkon: {{ states('sensor.kresse_temperature') }}°C, Tankstelle R.
        Waser: Diesel: {{ state_attr('sensor.r_waser', 'DIESEL') }} CHF, SP95:
        {{ state_attr('sensor.r_waser', 'SP95') }} CHF, SP98: {{
        state_attr('sensor.r_waser', 'SP98') }} CHF
mode: single
