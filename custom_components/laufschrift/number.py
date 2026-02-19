"""Platform for number entities."""
import logging
import aiohttp

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_BRIGHTNESS,
    DEFAULT_SPEED,
    DEFAULT_REPEAT,
    DEFAULT_DURATION,
    DEFAULT_TRANSPARENCY,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    _LOGGER.info("Setting up number platform")
    host = config_entry.data.get("host")
    port = config_entry.data.get("port", DEFAULT_PORT)
    name = config_entry.data.get("name")

    async_add_entities([
        # Bestehende Numbers
        LaufschriftBrightnessNumber(host, port, name, config_entry),
        LaufschriftSpeedNumber(host, port, name, config_entry),
        # Neue Numbers
        LaufschriftRepeatNumber(host, port, name, config_entry),
        LaufschriftDurationNumber(host, port, name, config_entry),
        LaufschriftTransparencyNumber(host, port, name, config_entry),
    ])


# =============================================================================
# Basis-Klasse für alle Number-Entitäten
# =============================================================================

class LaufschriftNumberBase(NumberEntity):
    """Base class for Laufschrift number entities."""

    def __init__(
        self,
        host: str,
        port: int,
        name: str,
        config_entry: ConfigEntry,
        number_name: str,
        min_value: float,
        max_value: float,
        step: float,
        default: float,
        icon: str,
        unit: str | None = None,
        mode: NumberMode = NumberMode.SLIDER,
    ) -> None:
        """Initialize the entity."""
        self._host = host
        self._port = port
        self._device_name = name
        self.config_entry = config_entry
        self._value = default
        
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_native_value = default
        self._attr_mode = mode
        self._attr_unique_id = f"laufschrift_{host}_{name}_{number_name.lower().replace(' ', '_')}"
        self._attr_name = f"{name} {number_name}"
        self._attr_icon = icon
        
        if unit:
            self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        return self._value

    async def _send_command(self, endpoint: str) -> None:
        """Send command to Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self._host}:{self._port}{endpoint}"
                _LOGGER.debug(f"Sending command: {url}")
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Error sending command: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")


# =============================================================================
# Helligkeit Number
# =============================================================================

class LaufschriftBrightnessNumber(LaufschriftNumberBase):
    """Representation of a Laufschrift brightness number."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = int(config_entry.options.get("brightness", DEFAULT_BRIGHTNESS))
        super().__init__(
            host, port, name, config_entry,
            number_name="Helligkeit Slider",
            min_value=0,
            max_value=255,
            step=1,
            default=default,
            icon="mdi:brightness-6",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the brightness value."""
        _LOGGER.debug(f"Setting brightness to: {value}")
        self._value = int(value)
        await self._send_command(f"/brightness/{int(value)}")
        self.async_write_ha_state()


# =============================================================================
# Geschwindigkeit Number
# =============================================================================

class LaufschriftSpeedNumber(LaufschriftNumberBase):
    """Representation of a Laufschrift speed number."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = int(config_entry.options.get("speed", DEFAULT_SPEED))
        super().__init__(
            host, port, name, config_entry,
            number_name="Geschwindigkeit Slider",
            min_value=1,
            max_value=10,
            step=1,
            default=default,
            icon="mdi:speedometer",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the speed value."""
        _LOGGER.debug(f"Setting speed to: {value}")
        self._value = int(value)
        await self._send_command(f"/speed/{int(value)}")
        self.async_write_ha_state()


# =============================================================================
# 🆕 Wiederholungen Number
# =============================================================================

class LaufschriftRepeatNumber(LaufschriftNumberBase):
    """Representation of a Laufschrift repeat number."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = int(config_entry.options.get("repeat", DEFAULT_REPEAT))
        super().__init__(
            host, port, name, config_entry,
            number_name="Wiederholungen",
            min_value=1,
            max_value=10,
            step=1,
            default=default,
            icon="mdi:repeat",
            unit="x",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the repeat value."""
        _LOGGER.debug(f"Setting repeat to: {value}")
        self._value = int(value)
        await self._send_command(f"/repeat/{int(value)}")
        self.async_write_ha_state()


# =============================================================================
# 🆕 Anzeigedauer Number
# =============================================================================

class LaufschriftDurationNumber(LaufschriftNumberBase):
    """Representation of a Laufschrift duration number."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = int(config_entry.options.get("duration", DEFAULT_DURATION))
        super().__init__(
            host, port, name, config_entry,
            number_name="Anzeigedauer",
            min_value=1,
            max_value=300,
            step=1,
            default=default,
            icon="mdi:timer-outline",
            unit="s",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the duration value."""
        _LOGGER.debug(f"Setting duration to: {value}")
        self._value = int(value)
        await self._send_command(f"/duration/{int(value)}")
        self.async_write_ha_state()


# =============================================================================
# 🆕 Hintergrund-Transparenz Number
# =============================================================================

class LaufschriftTransparencyNumber(LaufschriftNumberBase):
    """Representation of a Laufschrift transparency number."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = int(config_entry.options.get("transparency", DEFAULT_TRANSPARENCY))
        super().__init__(
            host, port, name, config_entry,
            number_name="Transparenz",
            min_value=0,
            max_value=100,
            step=1,
            default=default,
            icon="mdi:opacity",
            unit="%",
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the transparency value."""
        _LOGGER.debug(f"Setting transparency to: {value}")
        self._value = int(value)
        await self._send_command(f"/transparency/{int(value)}")
        self.async_write_ha_state()