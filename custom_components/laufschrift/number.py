"""Platform for number entity."""
import logging

import aiohttp
import voluptuous as vol

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Laufschrift number platform."""
    _LOGGER.info("Setting up number platform")
    host = config_entry.data.get("host")

    async_add_entities(
        [
            LaufschriftBrightnessNumber(host),
            LaufschriftSpeedNumber(host),
        ]
    )


class LaufschriftNumber(NumberEntity):
    """Base class for Laufschrift numbers."""

    _attr_has_entity_name = True  # Wichtig für neue Integrationen

    def __init__(self, host: str, name: str, mode: NumberMode, min_value: int, max_value: int) -> None:
        """Initialize the Laufschrift number."""
        self._host = host
        self._name = name
        self._attr_available = False
        self._attr_mode = mode
        self._attr_min_value = min_value
        self._attr_max_value = max_value
        self._value = None
        self._attr_unique_id = f"laufschrift_{name.lower()}"

    async def async_update(self) -> None:
        """Update the number's state."""
        try:
            new_value = await self.get_laufschrift_value()
            if new_value is not None:
                self._attr_available = True
                self._value = new_value
            else:
                self._attr_available = False
        except Exception as e:
            _LOGGER.error(f"Error updating number: {e}")
            self._attr_available = False

    async def get_laufschrift_value(self) -> str | None:
        """Get the value from the Laufschrift."""
        # Überschreibe diese Methode in den Unterklassen, um den spezifischen Wert abzurufen
        raise NotImplementedError()

    async def set_laufschrift_value(self, value: float) -> None:
        """Send the value to the Laufschrift."""
        # Überschreibe diese Methode in den Unterklassen, um den spezifischen Wert an die Laufschrift-App zu senden
        raise NotImplementedError()

    @property
    def state(self) -> str | None:
        """Return the state of the number."""
        return self._value

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self.set_laufschrift_value(value)
        self._attr_native_value = value
        self.async_write_ha_state()
class LaufschriftBrightnessNumber(LaufschriftNumber):
    """Representation of the Laufschrift brightness number."""

    def __init__(self, host: str) -> None:
        super().__init__(host, "Helligkeit", NumberMode.SLIDER, 0, 255)

    async def get_laufschrift_value(self) -> int | None:
        """Get the brightness from the Laufschrift."""
        # Hier musst Du die Logik implementieren, um die Helligkeit von Deiner Laufschrift-App abzurufen
        # Zum Beispiel durch Senden einer HTTP-Anfrage
        # Rückgabe der Helligkeit oder None, falls ein Fehler auftritt
        return 230  # Dummy-Wert

    async def set_laufschrift_value(self, value: float) -> None:
        """Send the brightness value to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/set_brightness/{int(value)}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting brightness: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")
class LaufschriftSpeedNumber(LaufschriftNumber):
    """Representation of the Laufschrift speed number."""

    def __init__(self, host: str) -> None:
        super().__init__(host, "Geschwindigkeit", NumberMode.SLIDER, 1, 10)
        self._attr_native_unit_of_measurement = UnitOfSpeed.MILES_PER_HOUR

    async def get_laufschrift_value(self) -> int | None:
        """Get the speed from the Laufschrift."""
        # Hier musst Du die Logik implementieren, um die Geschwindigkeit von Deiner Laufschrift-App abzurufen
        # Zum Beispiel durch Senden einer HTTP-Anfrage
        # Rückgabe der Geschwindigkeit oder None, falls ein Fehler auftritt
        return 3  # Dummy-Wert

    async def set_laufschrift_value(self, value: float) -> None:
        """Send the speed value to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/set_speed/{int(value)}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting speed: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")