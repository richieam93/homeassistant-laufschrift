"""Platform for switch entity."""
import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
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
    """Set up the switch platform."""
    _LOGGER.info("Setting up switch platform")
    host = config_entry.data.get("host")

    async_add_entities([LaufschriftShutdownSwitch(host)])


class LaufschriftShutdownSwitch(SwitchEntity):
    """Representation of a Laufschrift shutdown switch."""

    _attr_name = "PC herunterfahren"  # Geänderter Name
    _attr_unique_id = "laufschrift_shutdown_switch"

    def __init__(self, host: str) -> None:
        """Initialize the entity."""
        self._host = host
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Return True if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        _LOGGER.info("Shutting down the Laufschrift")
        self._is_on = True
        self.async_write_ha_state()
        await self.shutdown_laufschrift()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        _LOGGER.info("Shutdown cancelled")
        self._is_on = False
        self.async_write_ha_state()
        #Wenn du das Herunterfahren abbrechen möchtest, füge die Logik hier ein

    async def shutdown_laufschrift(self) -> None:
        """Send shutdown command to Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:5000/shutdown"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error setting text: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")