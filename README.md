# Home Assistant Laufschrift Integration 📝

[![HACS Default](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Diese Integration ermöglicht die Steuerung einer Laufschrift über Home Assistant. Sie ermöglicht das Einstellen von Text, Helligkeit, Geschwindigkeit und Farbe über eine benutzerdefinierte Komponente.

## ✨ Funktionen

*   **Text einstellen:** Ändere den angezeigten Text der Laufschrift.
*   **Helligkeit einstellen:** Passe die Helligkeit der Laufschrift an.
*   **Geschwindigkeit einstellen:** Ändere die Geschwindigkeit, mit der der Text auf der Laufschrift läuft.
*   **Farbe einstellen:** Wähle die Farbe des Textes auf der Laufschrift.
*   **PC herunterfahren:** Schalter zum Herunterfahren des PCs, auf dem die Laufschrift-Software läuft.

## ✅ Voraussetzungen

*   Home Assistant 2023.1 oder höher
*   HACS (Home Assistant Community Store)

## 🚀 Installation

1.  Füge dieses Repository als Custom Repository in HACS hinzu.
    *   Repository: `richieam93/homeassistant-laufschrift`
    *   Kategorie: Integration
2.  Installiere die "Laufschrift" Integration über HACS.
3.  Starte Home Assistant neu.

## ⚙️ Konfiguration

1.  **Software auf dem PC starten:**
    *   Vor der Installation der Integration muss die Laufschrift-Software auf dem PC gestartet werden. Diese befindet sich im Ordner `homeassistant-laufschrift\Laufschrift_exe`.
    *   Die Software kann entweder manuell oder über ein Skript gestartet werden.
2.  **Integration hinzufügen:**
    *   Gehe zu "Konfiguration" -> "Integrationen" in Home Assistant.
    *   Klicke auf den "+ Integration hinzufügen" Button und suche nach "Laufschrift".
    *   Gib die IP-Adresse Deines PCs ein, auf dem die Laufschrift-App ausgeführt wird.
3.  **Optionen konfigurieren:**
    *   Nach der Installation kannst du die Standardwerte für Helligkeit und Geschwindigkeit über die "Optionen" der Integration anpassen.

## 💡 Verwendung

Nach der Konfiguration werden folgende Entitäten erstellt:

*   `text.laufschrift_text`: Ermöglicht das Einstellen des Textes, der auf der Laufschrift angezeigt wird.
*   `select.laufschrift_brightness`: Ermöglicht die Auswahl der Helligkeit.
*   `select.laufschrift_speed`: Ermöglicht die Auswahl der Geschwindigkeit.
*   `select.laufschrift_color`: Ermöglicht die Auswahl der Farbe.
*   `switch.pc_herunterfahren`: Schalter zum Herunterfahren des PCs.

Du kannst diese Entitäten in Deinen Automatisierungen und Skripten verwenden.

## 📖 Beispiel Automation

```yaml
automation:
  - alias: "Temperaturen + Tankstelle auf Laufschrift"
    description: "Zeigt stündlich die Temperaturen verschiedener Sensoren auf der Laufschrift an"
    trigger:
      - platform: time_pattern
        minutes: "/50"
    action:
      - service: text.set_value
        data:
          entity_id: text.laufschrift_text
          value: >-
            Temperaturen: Wohnzimmer: {{ states('sensor.airpurifier_temperature') }}°C,
            Schlafzimmer: {{ states('sensor.stecker_mucken_device_temperature') }}°C,
            TV Sideboard: {{ states('sensor.stecker_tv_leds_device_temperature') }}°C,
            Caffè Maschine: {{ states('sensor.stecker_kaffe_device_temperature') }}°C,
            Balkon: {{ states('sensor.kresse_temperature') }}°C,
            Tankstelle R. Waser: Diesel: {{ state_attr('sensor.r_waser', 'DIESEL') }} CHF,
            SP95: {{ state_attr('sensor.r_waser', 'SP95') }} CHF,
            SP98: {{ state_attr('sensor.r_waser', 'SP98') }} CHF
    mode: single

## 🎨 Beispiel Steuerung
Anpassung von Helligkeit, Geschwindigkeit und Farbe
Um die Helligkeit, Geschwindigkeit und Farbe über Automatisierungen oder Skripte zu ändern, verwende den select.select_option Service. Hier sind Beispiele:

## Helligkeit ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_brightness
      option: "255"  # Wähle eine Helligkeitsstufe aus den verfügbaren Optionen

## Geschwindigkeit ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_speed
      option: "5"  # Wähle eine Geschwindigkeitsstufe aus den verfügbaren Optionen

## Farbe ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_color
      option: "Rot"  # Wähle eine Farbe aus den verfügbaren Optionen
