"""Platform for switch entity."""
import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    _LOGGER.info("Setting up switch platform")
    host = config_entry.data.get("host")
    port = config_entry.data.get("port", DEFAULT_PORT)
    name = config_entry.data.get("name")

    async_add_entities([
        LaufschriftShutdownSwitch(host, port, name, config_entry),
        LaufschriftPauseSwitch(host, port, name, config_entry),
    ])


class LaufschriftShutdownSwitch(SwitchEntity):
    """Representation of a Laufschrift shutdown switch."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._host = host
        self._port = port
        self._name = name
        self.config_entry = config_entry
        self._is_on = False
        self._attr_unique_id = f"laufschrift_{host}_{name}_shutdown"
        self._attr_name = f"{name} PC Herunterfahren"
        self._attr_icon = "mdi:power"

    @property
    def is_on(self) -> bool:
        """Return True if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        _LOGGER.info("Shutting down the Laufschrift PC")
        self._is_on = True
        self.async_write_ha_state()
        await self._send_command("/shutdown")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        _LOGGER.info("Shutdown switch turned off")
        self._is_on = False
        self.async_write_ha_state()

    async def _send_command(self, endpoint: str) -> None:
        """Send command to Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:{self._port}{endpoint}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error sending command: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")


class LaufschriftPauseSwitch(SwitchEntity):
    """Representation of a Laufschrift pause switch."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._host = host
        self._port = port
        self._name = name
        self.config_entry = config_entry
        self._is_on = False
        self._attr_unique_id = f"laufschrift_{host}_{name}_pause"
        self._attr_name = f"{name} Pausieren"
        self._attr_icon = "mdi:pause"

    @property
    def is_on(self) -> bool:
        """Return True if paused."""
        return self._is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Pause the display."""
        _LOGGER.info("Pausing the Laufschrift")
        self._is_on = True
        self.async_write_ha_state()
        await self._send_command("/pause")

    async def async_turn_off(self, **kwargs) -> None:
        """Resume the display."""
        _LOGGER.info("Resuming the Laufschrift")
        self._is_on = False
        self.async_write_ha_state()
        await self._send_command("/resume")

    async def _send_command(self, endpoint: str) -> None:
        """Send command to Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:{self._port}{endpoint}"
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error sending command: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")