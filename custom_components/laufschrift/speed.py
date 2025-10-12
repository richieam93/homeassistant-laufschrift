"""Platform for speed select entity."""
import logging

import aiohttp
import voluptuous as vol

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    _LOGGER.info("Setting up speed platform")
    host = config_entry.data.get("host")
    name = config_entry.data.get("name")

    async_add_entities([LaufschriftSpeedSelect(host, name, config_entry)])


class LaufschriftSpeedSelect(SelectEntity):
    """Representation of a Laufschrift speed select."""

    _attr_name = "Geschwindigkeit"
    _attr_options = ["1", "2", "3", "4", "5"]

    def __init__(self, host: str, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._host = host
        self._name = name
        self.config_entry = config_entry
        self._selected_speed = int(config_entry.options.get("speed", "3"))  # Als Integer speichern
        self._attr_unique_id = f"laufschrift_{host}_{name}_speed_select"

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        return str(self._selected_speed)  # Als String zurückgeben

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting speed to: {option}")
        self._selected_speed = int(option)  # Als Integer speichern
        await self.set_laufschrift_speed(self._selected_speed)  # Integer übergeben
        self.async_write_ha_state()

    async def set_laufschrift_speed(self, speed: int) -> None:
        """Send the speed to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/speed/{speed}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting speed: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")