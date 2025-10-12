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

    async_add_entities([LaufschriftSpeedNumber(host)])


class LaufschriftSpeedNumber(NumberEntity):
    """Representation of a Laufschrift speed number."""

    _attr_name = "Geschwindigkeit"
    _attr_unique_id = "laufschrift_speed_number"
    _attr_native_min_value = 1
    _attr_native_max_value = 10
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, host: str) -> None:
        """Initialize the entity."""
        self._host = host
        self._speed = 3  # Standardgeschwindigkeit

    @property
    def native_value(self) -> float | None:
        """Return the speed value."""
        return self._speed

    async def async_set_native_value(self, value: float) -> None:
        """Set the speed value."""
        _LOGGER.debug(f"Setting speed to: {value}")
        self._speed = value
        await self.set_laufschrift_speed(int(value))
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