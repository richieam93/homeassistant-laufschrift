"""Platform for number entity."""
import logging

import aiohttp
import voluptuous as vol

from homeassistant.components.number import NumberEntity, NumberMode
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
    """Set up the number platform."""
    _LOGGER.info("Setting up number platform")
    host = config_entry.data.get("host")

    async_add_entities([LaufschriftBrightnessNumber(host)])


class LaufschriftBrightnessNumber(NumberEntity):
    """Representation of a Laufschrift brightness number."""

    _attr_name = "Helligkeit"
    _attr_unique_id = "laufschrift_brightness_number"
    _attr_native_min_value = 0
    _attr_native_max_value = 255
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, host: str) -> None:
        """Initialize the entity."""
        self._host = host
        self._brightness = 230  # Standardhelligkeit

    @property
    def native_value(self) -> float | None:
        """Return the brightness value."""
        return self._brightness

    async def async_set_native_value(self, value: float) -> None:
        """Set the brightness value."""
        _LOGGER.debug(f"Setting brightness to: {value}")
        self._brightness = value
        await self.set_laufschrift_brightness(int(value))
        self.async_write_ha_state()

    async def set_laufschrift_brightness(self, brightness: int) -> None:
        """Send the brightness to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/brightness/{brightness}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting brightness: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")