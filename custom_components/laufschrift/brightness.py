"""Platform for brightness select entity."""
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
    _LOGGER.info("Setting up brightness platform")
    host = config_entry.data.get("host")

    async_add_entities([LaufschriftBrightnessSelect(host, config_entry)])


class LaufschriftBrightnessSelect(SelectEntity):
    """Representation of a Laufschrift brightness select."""

    _attr_name = "Helligkeit"
    _attr_unique_id = "laufschrift_brightness_select"
    _attr_options = ["30", "80", "130", "180", "230", "255"]

    def __init__(self, host: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._host = host
        self.config_entry = config_entry
        self._selected_brightness = config_entry.options.get("brightness", "230")  # Standardhelligkeit

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        return self._selected_brightness

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting brightness to: {option}")
        self._selected_brightness = option
        await self.set_laufschrift_brightness(option)
        self.async_write_ha_state()

    async def set_laufschrift_brightness(self, brightness: str) -> None:
        """Send the brightness to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/brightness/{brightness}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting brightness: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")
