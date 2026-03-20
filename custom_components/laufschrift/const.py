"""Constants for the Laufschrift integration."""

DOMAIN = "laufschrift"
PLATFORMS = ["text", "switch", "select", "number", "sensor"]

SERVICE_LAUFSCHRIFT_SET_TEXT = "set_text"
SERVICE_LAUFSCHRIFT_SHUTDOWN = "shutdown"
SERVICE_LAUFSCHRIFT_PAUSE = "pause"
SERVICE_LAUFSCHRIFT_RESUME = "resume"
SERVICE_LAUFSCHRIFT_WAKESCREEN = "set_wakescreen"

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

OPTIONS_MODE = ["Scroll", "Statisch"]
OPTIONS_TEXTSIZE = ["Klein", "Mittel", "Groß"]
OPTIONS_POSITION = ["Oben", "Mitte", "Unten"]
OPTIONS_DIRECTION = ["Links → Rechts", "Rechts → Links"]
OPTIONS_PRIORITY = ["Normal", "Hoch", "Kritisch"]
OPTIONS_BRIGHTNESS = ["30", "80", "130", "180", "230", "255"]
OPTIONS_SPEED = ["1", "2", "3", "4", "5"]

OPTIONS_COLOR = [
    "Weiss",
    "Warmweiss",
    "Rot",
    "Dunkelrot",
    "Orange",
    "Gelb",
    "Gold",
    "Lime",
    "Gruen",
    "Dunkelgruen",
    "Tuerkis",
    "Cyan",
    "Hellblau",
    "Blau",
    "Dunkelblau",
    "Lila",
    "Violett",
    "Magenta",
    "Pink",
    "Rosa",
    "Koralle",
    "Lachs",
    "Bernstein",
    "Mint",
    "Schwarz",
]

MODE_MAPPING = {
    "Scroll": "scroll",
    "Statisch": "static",
}

TEXTSIZE_MAPPING = {
    "Klein": "klein",
    "Mittel": "mittel",
    "Gross": "gross",
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
    "Weiss": {"red": 255, "green": 255, "blue": 255},
    "Warmweiss": {"red": 255, "green": 244, "blue": 229},
    "Rot": {"red": 255, "green": 0, "blue": 0},
    "Dunkelrot": {"red": 139, "green": 0, "blue": 0},
    "Orange": {"red": 255, "green": 165, "blue": 0},
    "Gelb": {"red": 255, "green": 255, "blue": 0},
    "Gold": {"red": 255, "green": 215, "blue": 0},
    "Lime": {"red": 191, "green": 255, "blue": 0},
    "Gruen": {"red": 0, "green": 255, "blue": 0},
    "Dunkelgruen": {"red": 0, "green": 100, "blue": 0},
    "Tuerkis": {"red": 64, "green": 224, "blue": 208},
    "Cyan": {"red": 0, "green": 255, "blue": 255},
    "Hellblau": {"red": 135, "green": 206, "blue": 250},
    "Blau": {"red": 0, "green": 0, "blue": 255},
    "Dunkelblau": {"red": 0, "green": 0, "blue": 139},
    "Lila": {"red": 128, "green": 0, "blue": 128},
    "Violett": {"red": 138, "green": 43, "blue": 226},
    "Magenta": {"red": 255, "green": 0, "blue": 255},
    "Pink": {"red": 255, "green": 20, "blue": 147},
    "Rosa": {"red": 255, "green": 192, "blue": 203},
    "Koralle": {"red": 255, "green": 127, "blue": 80},
    "Lachs": {"red": 250, "green": 128, "blue": 114},
    "Bernstein": {"red": 255, "green": 191, "blue": 0},
    "Mint": {"red": 152, "green": 255, "blue": 152},
    "Schwarz": {"red": 0, "green": 0, "blue": 0},
}

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
ENDPOINT_WAKESCREEN = "/wakescreen/{value}"
