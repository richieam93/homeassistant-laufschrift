"""Constants for the Laufschrift integration."""

DOMAIN = "laufschrift"
PLATFORMS = ["text", "switch", "select", "number", "sensor"]

# Services
SERVICE_LAUFSCHRIFT_SET_TEXT = "set_text"
SERVICE_LAUFSCHRIFT_SHUTDOWN = "shutdown"
SERVICE_LAUFSCHRIFT_PAUSE = "pause"
SERVICE_LAUFSCHRIFT_RESUME = "resume"

# Default Werte
DEFAULT_PORT = 5000
DEFAULT_BRIGHTNESS = 230
DEFAULT_SPEED = 3
DEFAULT_REPEAT = 1
DEFAULT_DURATION = 10
DEFAULT_TRANSPARENCY = 0
DEFAULT_MODE = "scroll"
DEFAULT_TEXTSIZE = "mittel"
DEFAULT_POSITION = "oben"
DEFAULT_DIRECTION = "ltr"
DEFAULT_PRIORITY = "normal"
DEFAULT_COLOR = "Weiss"

# Optionen für Select-Entitäten
OPTIONS_MODE = ["Scroll", "Statisch"]
OPTIONS_TEXTSIZE = ["Klein", "Mittel", "Groß"]
OPTIONS_POSITION = ["Oben", "Mitte", "Unten"]
OPTIONS_DIRECTION = ["Links → Rechts", "Rechts → Links"]
OPTIONS_PRIORITY = ["Normal", "Hoch", "Kritisch"]
OPTIONS_COLOR = ["Rot", "Grün", "Blau", "Weiss"]
OPTIONS_BRIGHTNESS = ["30", "80", "130", "180", "230", "255"]
OPTIONS_SPEED = ["1", "2", "3", "4", "5"]

# Mapping für API-Calls (Deutsche UI → API-Wert)
MODE_MAPPING = {
    "Scroll": "scroll",
    "Statisch": "static",
}

TEXTSIZE_MAPPING = {
    "Klein": "klein",
    "Mittel": "mittel",
    "Groß": "gross",
}

POSITION_MAPPING = {
    "Oben": "oben",
    "Mitte": "mitte",
    "Unten": "unten",
}

DIRECTION_MAPPING = {
    "Links → Rechts": "ltr",
    "Rechts → Links": "rtl",
}

PRIORITY_MAPPING = {
    "Normal": "normal",
    "Hoch": "hoch",
    "Kritisch": "kritisch",
}

COLOR_MAPPING = {
    "Rot": {"red": 255, "green": 0, "blue": 0},
    "Grün": {"red": 0, "green": 255, "blue": 0},
    "Blau": {"red": 0, "green": 0, "blue": 255},
    "Weiss": {"red": 255, "green": 255, "blue": 255},
}

# API Endpunkte
ENDPOINT_TEXT = "/text/{value}"
ENDPOINT_BRIGHTNESS = "/brightness/{value}"
ENDPOINT_SPEED = "/speed/{value}"
ENDPOINT_RED = "/red/{value}"
ENDPOINT_GREEN = "/green/{value}"
ENDPOINT_BLUE = "/blue/{value}"
ENDPOINT_MODE = "/mode/{value}"
ENDPOINT_REPEAT = "/repeat/{value}"
ENDPOINT_DURATION = "/duration/{value}"
ENDPOINT_TEXTSIZE = "/textsize/{value}"
ENDPOINT_POSITION = "/position/{value}"
ENDPOINT_DIRECTION = "/direction/{value}"
ENDPOINT_PRIORITY = "/priority/{value}"
ENDPOINT_TRANSPARENCY = "/transparency/{value}"
ENDPOINT_SHUTDOWN = "/shutdown"
ENDPOINT_PAUSE = "/pause"
ENDPOINT_RESUME = "/resume"