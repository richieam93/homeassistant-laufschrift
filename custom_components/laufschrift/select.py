"""Platform for select entities."""
import logging
import aiohttp

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    OPTIONS_COLOR,
    OPTIONS_BRIGHTNESS,
    OPTIONS_SPEED,
    OPTIONS_MODE,
    OPTIONS_TEXTSIZE,
    OPTIONS_POSITION,
    OPTIONS_DIRECTION,
    OPTIONS_PRIORITY,
    COLOR_MAPPING,
    MODE_MAPPING,
    TEXTSIZE_MAPPING,
    POSITION_MAPPING,
    DIRECTION_MAPPING,
    PRIORITY_MAPPING,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    _LOGGER.info("Setting up select platform")
    host = config_entry.data.get("host")
    port = config_entry.data.get("port", DEFAULT_PORT)
    name = config_entry.data.get("name")

    async_add_entities([
        # Bestehende Selects
        LaufschriftColorSelect(host, port, name, config_entry),
        LaufschriftBrightnessSelect(host, port, name, config_entry),
        LaufschriftSpeedSelect(host, port, name, config_entry),
        # Neue Selects
        LaufschriftModeSelect(host, port, name, config_entry),
        LaufschriftTextsizeSelect(host, port, name, config_entry),
        LaufschriftPositionSelect(host, port, name, config_entry),
        LaufschriftDirectionSelect(host, port, name, config_entry),
        LaufschriftPrioritySelect(host, port, name, config_entry),
    ])


# =============================================================================
# Basis-Klasse für alle Select-Entitäten
# =============================================================================

class LaufschriftSelectBase(SelectEntity):
    """Base class for Laufschrift select entities."""

    def __init__(
        self,
        host: str,
        port: int,
        name: str,
        config_entry: ConfigEntry,
        select_name: str,
        options: list,
        default: str,
        icon: str,
    ) -> None:
        """Initialize the entity."""
        self._host = host
        self._port = port
        self._device_name = name
        self.config_entry = config_entry
        self._selected = default
        self._attr_options = options
        self._attr_unique_id = f"laufschrift_{host}_{name}_{select_name.lower().replace(' ', '_')}"
        self._attr_name = f"{name} {select_name}"
        self._attr_icon = icon

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        return self._selected

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
# Farbe Select
# =============================================================================

class LaufschriftColorSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift color select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Farbe",
            options=OPTIONS_COLOR,
            default="Weiss",
            icon="mdi:palette",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting color to: {option}")
        self._selected = option
        
        # Hole RGB-Werte aus dem Mapping
        color = COLOR_MAPPING.get(option, COLOR_MAPPING["Weiss"])
        await self._send_command(f"/red/{color['red']}")
        await self._send_command(f"/green/{color['green']}")
        await self._send_command(f"/blue/{color['blue']}")
        
        self.async_write_ha_state()


# =============================================================================
# Helligkeit Select
# =============================================================================

class LaufschriftBrightnessSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift brightness select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = config_entry.options.get("brightness", "230")
        super().__init__(
            host, port, name, config_entry,
            select_name="Helligkeit",
            options=OPTIONS_BRIGHTNESS,
            default=default,
            icon="mdi:brightness-6",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting brightness to: {option}")
        self._selected = option
        await self._send_command(f"/brightness/{option}")
        self.async_write_ha_state()


# =============================================================================
# Geschwindigkeit Select
# =============================================================================

class LaufschriftSpeedSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift speed select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        default = config_entry.options.get("speed", "3")
        super().__init__(
            host, port, name, config_entry,
            select_name="Geschwindigkeit",
            options=OPTIONS_SPEED,
            default=default,
            icon="mdi:speedometer",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting speed to: {option}")
        self._selected = option
        await self._send_command(f"/speed/{option}")
        self.async_write_ha_state()


# =============================================================================
# 🆕 Anzeigemodus Select (Scroll / Statisch)
# =============================================================================

class LaufschriftModeSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift mode select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Anzeigemodus",
            options=OPTIONS_MODE,
            default="Scroll",
            icon="mdi:animation-play",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting mode to: {option}")
        self._selected = option
        
        # Mapping: "Scroll" -> "scroll", "Statisch" -> "static"
        api_value = MODE_MAPPING.get(option, "scroll")
        await self._send_command(f"/mode/{api_value}")
        
        self.async_write_ha_state()


# =============================================================================
# 🆕 Textgröße Select
# =============================================================================

class LaufschriftTextsizeSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift textsize select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Textgröße",
            options=OPTIONS_TEXTSIZE,
            default="Mittel",
            icon="mdi:format-size",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting textsize to: {option}")
        self._selected = option
        
        # Mapping: "Klein" -> "klein", "Mittel" -> "mittel", "Groß" -> "gross"
        api_value = TEXTSIZE_MAPPING.get(option, "mittel")
        await self._send_command(f"/textsize/{api_value}")
        
        self.async_write_ha_state()


# =============================================================================
# 🆕 Position Select
# =============================================================================

class LaufschriftPositionSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift position select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Position",
            options=OPTIONS_POSITION,  # ["Oben", "Mitte", "Unten"]
            default="Oben",
            icon="mdi:format-vertical-align-center",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting position to: {option}")
        self._selected = option
        
        # Mapping: "Oben" -> "oben", "Mitte" -> "mitte", "Unten" -> "unten"
        api_value = POSITION_MAPPING.get(option, "oben")
        await self._send_command(f"/position/{api_value}")
        
        self.async_write_ha_state()


# =============================================================================
# 🆕 Scroll-Richtung Select
# =============================================================================

class LaufschriftDirectionSelect(LaufschriftSelectBase):
    """Representation of a Laufschrift direction select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Scroll-Richtung",
            options=OPTIONS_DIRECTION,
            default="Links → Rechts",
            icon="mdi:arrow-left-right",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting direction to: {option}")
        self._selected = option
        
        # Mapping: "Links → Rechts" -> "ltr", "Rechts → Links" -> "rtl"
        api_value = DIRECTION_MAPPING.get(option, "ltr")
        await self._send_command(f"/direction/{api_value}")
        
        self.async_write_ha_state()


# =============================================================================
# 🆕 Priorität Select
# =============================================================================

class LaufschriftPrioritySelect(LaufschriftSelectBase):
    """Representation of a Laufschrift priority select."""

    def __init__(self, host: str, port: int, name: str, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        super().__init__(
            host, port, name, config_entry,
            select_name="Priorität",
            options=OPTIONS_PRIORITY,
            default="Normal",
            icon="mdi:priority-high",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug(f"Setting priority to: {option}")
        self._selected = option
        
        # Mapping: "Normal" -> "normal", "Hoch" -> "hoch", "Kritisch" -> "kritisch"
        api_value = PRIORITY_MAPPING.get(option, "normal")
        await self._send_command(f"/priority/{api_value}")
        
        self.async_write_ha_state()