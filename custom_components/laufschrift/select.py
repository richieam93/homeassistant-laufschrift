"""Platform for color select entity."""
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
    _LOGGER.info("Setting up select platform")
    host = config_entry.data.get("host")
    name = config_entry.data.get("name")  # Hole den Namen aus der ConfigEntry

    async_add_entities([LaufschriftColorSelect(host, name, config_entry)])


class LaufschriftColorSelect(SelectEntity):
    """Representation of a Laufschrift color select."""

    _attr_options = ["Rot", "Grün", "Blau", "Weiss"]

    def __init__(self, host: str, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._host = host
        self._name = name
        self.config_entry = config_entry
        self._selected_color = "Weiss"  # Standardfarbe
        self._attr_unique_id = f"laufschrift_{host}_{name}_color_select"  # Eindeutige ID
        self._attr_name = f"{name} Farbe"  # Anzeigename

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        return self._selected_color

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting color to: {option}")
        self._selected_color = option
        await self.set_laufschrift_color(option)
        self.async_write_ha_state()

    async def set_laufschrift_color(self, color: str) -> None:
        """Send the color to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                if color == "Rot":
                    red, green, blue = 255, 0, 0
                elif color == "Grün":
                    red, green, blue = 0, 255, 0
                elif color == "Blau":
                    red, green, blue = 0, 0, 255
                else:  # Weiss
                    red, green, blue = 255, 255, 255

                url_red = f"http://{self._host}:5000/red/{red}"
                url_green = f"http://{self._host}:5000/green/{green}"
                url_blue = f"http://{self._host}:5000/blue/{blue}"

                await session.get(url_red)
                await session.get(url_green)
                await session.get(url_blue)
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")