# Home Assistant Laufschrift Integration 📝

🖥️ **Display scrolling text notifications on your TV/PC**

🖥️ **Laufschrift-Benachrichtigungen auf deinem TV/PC anzeigen**

[English](#-english) | [Deutsch](#-deutsch)

---

## ⚠️ Status

| Feature | Status |
|---------|--------|
| 🇩🇪 German UI | ✅ Ready |
| 🇬🇧 English UI | 🚧 Coming soon |
| 🖥️ Windows | ✅ Ready |
| 🐧 Linux/Mac | 🚧 Coming soon |

---

# 🇬🇧 English

This integration allows you to display scrolling text notifications on any Windows PC or TV connected to a PC.

**Perfect for:** Media rooms, living rooms, offices – get notifications without interrupting what you're watching!

---

## 🎯 What does it do?

Send text from Home Assistant to your PC/TV. The text appears briefly as a scrolling banner at the top of the screen, then disappears automatically.

| Feature | Description |
|---------|-------------|
| 📝 **Scrolling Text** | Display any text as notification |
| 🎨 **Custom Colors** | RGB color picker |
| 💡 **Brightness** | Adjustable brightness |
| ⚡ **Speed** | Adjustable scroll speed |
| 🔌 **PC Shutdown** | Shutdown PC remotely via Home Assistant |

---

## ✨ How it works

1. **PC Software** runs in background (minimized)
2. **Home Assistant** sends text via integration
3. **Text appears** briefly at top of screen
4. **Auto-hides** after text is displayed
5. **Non-intrusive** – doesn't interrupt your movie!

---

## 📸 Screenshots

### Home Assistant Integration
![Einstellungen](images/Einstellungen.PNG)

### Entities
![Entitäten](images/Entitäten.PNG)

### Scrolling Text on Screen
![Laufschrift](images/laufschrift.PNG)

### Web Configuration
![Webserver](images/Webserver.PNG)

---

## 📋 Requirements

| Requirement | Details |
|-------------|---------|
| **Home Assistant** | 2023.1 or higher |
| **HACS** | Home Assistant Community Store |
| **Windows PC** | For the display software |

---

## 🚀 Installation

### Step 1: Install PC Software

1. Download from: Laufschrift_exe/laufschrift_app.exe
2. Run on your Windows PC
3. The app minimizes automatically to background

### Step 2: Install Home Assistant Integration

1. Add this repository to HACS:
   - Repository: richieam93/homeassistant-laufschrift
   - Category: Integration
2. Install "Laufschrift" via HACS
3. Restart Home Assistant

### Step 3: Configure

1. Go to **Settings → Integrations**
2. Click **"+ Add Integration"**
3. Search for **"Laufschrift"**
4. Enter PC IP address and name

---

## ⚙️ Entities

After setup, these entities are created:

| Entity | Description |
|--------|-------------|
| text.laufschrift_NAME_text | Set the display text |
| select.laufschrift_NAME_brightness | Set brightness |
| select.laufschrift_NAME_speed | Set scroll speed |
| select.laufschrift_NAME_color | Set text color |
| switch.laufschrift_NAME_pc_herunterfahren | Shutdown PC |

---

## 🤖 Automation Example

See examples folder for automation YAML files.

---

# 🇩🇪 Deutsch

Diese Integration ermöglicht die Anzeige von Laufschrift-Benachrichtigungen auf jedem Windows PC oder TV, der mit einem PC verbunden ist.

**Perfekt für:** Wohnzimmer, Büro, Medienraum – Benachrichtigungen ohne Unterbrechung!

---

## 🎯 Was macht es?

Sende Text von Home Assistant an deinen PC/TV. Der Text erscheint kurz als Laufschrift am oberen Bildschirmrand und verschwindet dann automatisch.

| Feature | Beschreibung |
|---------|--------------|
| 📝 **Laufschrift** | Beliebigen Text anzeigen |
| 🎨 **Farben** | RGB Farbauswahl |
| 💡 **Helligkeit** | Einstellbare Helligkeit |
| ⚡ **Geschwindigkeit** | Einstellbare Laufgeschwindigkeit |
| 🔌 **PC Shutdown** | PC ferngesteuert herunterfahren |

---

## ✨ So funktioniert es

1. **PC Software** läuft im Hintergrund (minimiert)
2. **Home Assistant** sendet Text über Integration
3. **Text erscheint** kurz am oberen Bildschirmrand
4. **Verschwindet automatisch** nach Anzeige
5. **Nicht störend** – unterbricht keinen Film!

---

## 📸 Screenshots

### Home Assistant Integration
![Einstellungen](images/Einstellungen.PNG)

### Entitäten
![Entitäten](images/Entitäten.PNG)

### Laufschrift auf dem Bildschirm
![Laufschrift](images/laufschrift.PNG)

### Web-Konfiguration
![Webserver](images/Webserver.PNG)

---

## 📋 Voraussetzungen

| Anforderung | Details |
|-------------|---------|
| **Home Assistant** | 2023.1 oder höher |
| **HACS** | Home Assistant Community Store |
| **Windows PC** | Für die Anzeige-Software |

---

## 🚀 Installation

### Schritt 1: PC Software installieren

1. Download: Laufschrift_exe/laufschrift_app.exe
2. Auf Windows PC ausführen
3. App minimiert sich automatisch

### Schritt 2: Home Assistant Integration installieren

1. Repository zu HACS hinzufügen:
   - Repository: richieam93/homeassistant-laufschrift
   - Kategorie: Integration
2. "Laufschrift" über HACS installieren
3. Home Assistant neu starten

### Schritt 3: Konfigurieren

1. Gehe zu **Einstellungen → Integrationen**
2. Klicke **"+ Integration hinzufügen"**
3. Suche nach **"Laufschrift"**
4. PC IP-Adresse und Name eingeben

---

## ⚙️ Entitäten

Nach der Einrichtung werden diese Entitäten erstellt:

| Entität | Beschreibung |
|---------|--------------|
| text.laufschrift_NAME_text | Text einstellen |
| select.laufschrift_NAME_brightness | Helligkeit einstellen |
| select.laufschrift_NAME_speed | Geschwindigkeit einstellen |
| select.laufschrift_NAME_color | Farbe einstellen |
| switch.laufschrift_NAME_pc_herunterfahren | PC herunterfahren |

---

## 🤖 Automatisierungs-Beispiel

Siehe examples Ordner für Automatisierungs-YAML Dateien.

---

## ☕ Support this Project / Unterstütze dieses Projekt

This project is **free and open source**. Dieses Projekt ist **gratis und Open Source**.

If it helps you, I'd appreciate a coffee. Wenn es dir hilft, freue ich mich über einen Kaffee:

<a href="https://www.buymeacoffee.com/geartec" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>

---

## 📝 Feedback & Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/richieam93/homeassistant-laufschrift/issues)
- 💬 **Questions / Fragen:** Just open an issue!

---

## 📜 License / Lizenz

MIT License

---

Made with ❤️ in Switzerland 🇨🇭 | Entwickelt mit ❤️ in der Schweiz 🇨🇭


## ✨ Funktionen

*   **Text einstellen:** Ändere den angezeigten Text der Laufschrift.
*   **Helligkeit einstellen:** Passe die Helligkeit der Laufschrift an.
*   **Geschwindigkeit einstellen:** Ändere die Geschwindigkeit, mit der der Text auf der Laufschrift läuft.
*   **Farbe einstellen:** Wähle die Farbe des Textes auf der Laufschrift.
*   **PC herunterfahren:** Schalter zum Herunterfahren des PCs, auf dem die Laufschrift-Software läuft.

## Software-Verhalten 🖥️

Die Laufschrift-Software auf deinem PC zeigt den Text in einem Fenster an. Folgendes Verhalten ist zu beachten:

*   **Initialisierung:** Nach dem Start minimiert sich das Fenster automatisch in den Hintergrund.
*   **Textanzeige:** Wenn ein neuer Text über Home Assistant gesendet wird, erscheint das Fenster kurzzeitig (Pop-up), zeigt den Text einmalig an und minimiert sich danach wieder automatisch in den Hintergrund.
*   **Einmalige Anzeige:** Der Text wird nur einmal angezeigt, nicht in einer Endlosschleife.

## ✅ Voraussetzungen

*   Home Assistant 2023.1 oder höher
*   HACS (Home Assistant Community Store)

## 🚀 Installation

1.  Füge dieses Repository als Custom Repository in HACS hinzu:
    *   Repository: `richieam93/homeassistant-laufschrift`
    *   Kategorie: Integration
2.  Installiere die "Laufschrift" Integration über HACS.
3.  Starte Home Assistant neu.

## ⚙️ Konfiguration

1.  **Laufschrift-Software starten:**
    *   Stelle sicher, dass die Laufschrift-Software auf dem PC gestartet ist, bevor du die Integration installierst. Du findest sie im Ordner `homeassistant-laufschrift\Laufschrift_exe`.
    *   Du kannst die Software manuell starten oder ein Skript verwenden.
2.  **Integration hinzufügen:**
    *   Gehe zu "Konfiguration" -> "Integrationen" in Home Assistant.
    *   Klicke auf den "+ Integration hinzufügen" Button und suche nach "Laufschrift".
    *   Gib die IP-Adresse und den Namen deines PCs ein, auf dem die Laufschrift-App ausgeführt wird.
3.  **Optionen konfigurieren:**
    *   Nach der Installation kannst du die Standardwerte für Helligkeit und Geschwindigkeit über die "Optionen" der Integration anpassen.

## 💡 Verwendung

Nach der Konfiguration werden folgende Entitäten erstellt (beachte, dass `NAME` durch den von dir vergebenen Namen ersetzt wird):
*   `text.laufschrift_NAME_text`: Ermöglicht das Einstellen des Textes, der auf der Laufschrift angezeigt wird.
*   `select.laufschrift_NAME_brightness`: Ermöglicht die Auswahl der Helligkeit.
*   `select.laufschrift_NAME_speed`: Ermöglicht die Auswahl der Geschwindigkeit.
*   `select.laufschrift_NAME_color`: Ermöglicht die Auswahl der Farbe.
*   `switch.laufschrift_NAME_pc_herunterfahren`: Schalter zum Herunterfahren des PCs.

Du kannst diese Entitäten in deinen Automatisierungen und Skripten verwenden.


### Text Automation:

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
          entity_id: text.laufschrift_NAME_text  # Ersetze NAME
          value: >-
            Temperaturen: Wohnzimmer: {{ states('sensor.airpurifier_temperature') }}°C,
            Schlafzimmer: {{ states('sensor.stecker_mucken_device_temperature') }}°C,
            TV Sideboard: {{ states('sensor.stecker_tv_leds_device_temperature') }}°C,
            Caffè Maschine: {{ states('sensor.stecker_kaffe_device_temperature') }}°C,
            Balkon: {{ states('sensor.kresse_temperature') }}°C,
            Tankstelle R. Waser: Diesel: {{ state_attr('sensor.r_waser', 'DIESEL') }} CHF,
            SP95: {{ state_attr('sensor.r_waser', 'SP95') }} CHF
    mode: single

    Helligkeit, Geschwindigkeit und Farbe ändern:
Um die Helligkeit, Geschwindigkeit und Farbe über Automatisierungen oder Skripte zu ändern, verwende den select.select_option Service. Hier sind Beispiele:

Helligkeit ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_NAME_brightness  # Ersetze NAME
      option: "255"  # Wähle eine Helligkeitsstufe aus den verfügbaren Optionen

Geschwindigkeit ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_NAME_speed  # Ersetze NAME
      option: "5"  # Wähle eine Geschwindigkeitsstufe aus den verfügbaren Optionen

Farbe ändern:
action:
  - service: select.select_option
    data:
      entity_id: select.laufschrift_NAME_color  # Ersetze NAME
      option: "Rot"  # Wähle eine Farbe aus den verfügbaren Optionen
