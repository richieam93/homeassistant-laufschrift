"""Platform for sensor integration."""
import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
# from homeassistant.const import UNIT_LUMEN  # Nicht mehr direkt benötigt
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.info("Setting up sensor platform")
    host = config_entry.data.get("host")

    async_add_entities(
        [
            LaufschriftTextSensor(host),
            LaufschriftBrightnessSensor(host),
            LaufschriftSpeedSensor(host),
        ]
    )


class LaufschriftSensor(SensorEntity):
    """Base class for Laufschrift sensors."""

    _attr_has_entity_name = True  # Wichtig für neue Integrationen

    def __init__(self, host: str, name: str) -> None:
        """Initialize the sensor."""
        self._host = host
        self._name = name
        self._attr_available = False  # Starte im nicht verfügbaren Zustand
        self._value = None
        self._attr_unique_id = f"laufschrift_{name.lower()}"  # Unique ID mit laufschrift_ beginnen

    async def async_update(self) -> None:
        """Update the sensor's state."""
        try:
            new_value = await self.get_laufschrift_value()
            if new_value is not None:
                self._attr_available = True
                self._value = new_value
            else:
                self._attr_available = False  # Wert konnte nicht abgerufen werden
        except Exception as e:
            _LOGGER.error(f"Error updating sensor: {e}")
            self._attr_available = False

    async def get_laufschrift_value(self):
        """Get the value from the Laufschrift."""
        # Überschreibe diese Methode in den Unterklassen, um den spezifischen Wert abzurufen
        raise NotImplementedError()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Laufschrift {self._name}"


class LaufschriftTextSensor(LaufschriftSensor):
    """Representation of the Laufschrift text."""

    def __init__(self, host: str) -> None:
        super().__init__(host, "Text")
    _attr_unique_id = "laufschrift_text"

    async def get_laufschrift_value(self) -> str | None:
        """Get the text from the Laufschrift."""
        # Hier musst Du die Logik implementieren, um den Text von Deiner Laufschrift-App abzurufen
        # Zum Beispiel durch Senden einer HTTP-Anfrage
        # Rückgabe des Textes oder None, falls ein Fehler auftritt
        return "Hallo, Welt!"  # Dummy-Wert


class LaufschriftBrightnessSensor(LaufschriftSensor):
    """Representation of the Laufschrift brightness."""

    def __init__(self, host: str) -> None:
        super().__init__(host, "Brightness")
    _attr_unique_id = "laufschrift_brightness"
    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    #_attr_native_unit_of_measurement = "lm"
    @property
    def native_unit_of_measurement(self):
      return None

    async def get_laufschrift_value(self) -> int | None:
        """Get the brightness from the Laufschrift."""
        # Hier musst Du die Logik implementieren, um die Helligkeit von Deiner Laufschrift-App abzurufen
        # Zum Beispiel durch Senden einer HTTP-Anfrage
        # Rückgabe der Helligkeit oder None, falls ein Fehler auftritt
        return 230  # Dummy-Wert


class LaufschriftSpeedSensor(LaufschriftSensor):
    """Representation of the Laufschrift speed."""

    def __init__(self, host: str) -> None:
        super().__init__(host, "Speed")
    _attr_unique_id = "laufschrift_speed"
    _attr_state_class = SensorStateClass.MEASUREMENT

    async def get_laufschrift_value(self) -> int | None:
        """Get the speed from the Laufschrift."""
        # Hier musst Du die Logik implementieren, um die Geschwindigkeit von Deiner Laufschrift-App abzurufen
        # Zum Beispiel durch Senden einer HTTP-Anfrage
        # Rückgabe der Geschwindigkeit oder None, falls ein Fehler auftritt
        return 3  # Dummy-Wert