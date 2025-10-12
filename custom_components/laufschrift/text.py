"""Platform for text entity."""
import logging

import aiohttp

from homeassistant.components.text import TextEntity
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
    """Set up the text platform."""
    _LOGGER.info("Setting up text platform")
    host = config_entry.data.get("host")

    async_add_entities([LaufschriftTextEntity(host)])


class LaufschriftTextEntity(TextEntity):
    """Representation of a Laufschrift text entity."""

    _attr_name = "Text"
    _attr_unique_id = "laufschrift_text_input"

    def __init__(self, host: str) -> None:
        """Initialize the entity."""
        self._host = host
        self._text = "Hallo, Welt!"  # Standardtext

    @property
    def native_value(self) -> str | None:
        """Return the text value."""
        return self._text

    async def async_set_value(self, value: str) -> None:
        """Set the text value."""
        _LOGGER.debug(f"Setting text to: {value}")
        self._text = value
        # Hier musst Du den Text an Deine Laufschrift-App senden
        await self.set_laufschrift_text(value)
        self.async_write_ha_state()

    async def set_laufschrift_text(self, text: str) -> None:
        """Send the text to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/text/{text}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting text: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")