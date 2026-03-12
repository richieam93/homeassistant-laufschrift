"""Adds config flow for Laufschrift."""
import logging
import aiohttp

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_BRIGHTNESS,
    DEFAULT_SPEED,
    DEFAULT_REPEAT,
    DEFAULT_DURATION,
    DEFAULT_TRANSPARENCY,
    DEFAULT_MODE,
    DEFAULT_TEXTSIZE,
    DEFAULT_POSITION,
    DEFAULT_DIRECTION,
    DEFAULT_PRIORITY,
    OPTIONS_MODE,
    OPTIONS_TEXTSIZE,
    OPTIONS_POSITION,
    OPTIONS_DIRECTION,
    OPTIONS_PRIORITY,
    OPTIONS_BRIGHTNESS,
    OPTIONS_SPEED,
)

_LOGGER = logging.getLogger(__name__)


class LaufschriftConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Laufschrift."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}
        if user_input is not None:
            try:
                # Teste die Verbindung zur Laufschrift
                valid = await self._test_connect(
                    user_input[CONF_HOST], 
                    user_input.get(CONF_PORT, DEFAULT_PORT)
                )
                if not valid:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input
                    )
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_NAME, default="Laufschrift"): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                }
            ),
            errors=errors,
        )

    async def _test_connect(self, host: str, port: int) -> bool:
        """Test connection to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://{host}:{port}/",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
        except Exception as e:
            _LOGGER.error(f"Connection test failed: {e}")
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle options flow."""
        return LaufschriftOptionsFlow()


class LaufschriftOptionsFlow(config_entries.OptionsFlow):
    """Options flow for Laufschrift."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    # Anzeigemodus
                    vol.Optional(
                        "mode",
                        default=self.config_entry.options.get("mode", DEFAULT_MODE)
                    ): vol.In(OPTIONS_MODE),
                    
                    # Helligkeit
                    vol.Optional(
                        "brightness",
                        default=self.config_entry.options.get("brightness", str(DEFAULT_BRIGHTNESS))
                    ): vol.In(OPTIONS_BRIGHTNESS),
                    
                    # Geschwindigkeit
                    vol.Optional(
                        "speed",
                        default=self.config_entry.options.get("speed", str(DEFAULT_SPEED))
                    ): vol.In(OPTIONS_SPEED),
                    
                    # Textgröße
                    vol.Optional(
                        "textsize",
                        default=self.config_entry.options.get("textsize", DEFAULT_TEXTSIZE)
                    ): vol.In(OPTIONS_TEXTSIZE),
                    
                    # Position
                    vol.Optional(
                        "position",
                        default=self.config_entry.options.get("position", DEFAULT_POSITION)
                    ): vol.In(OPTIONS_POSITION),
                    
                    # Scroll-Richtung
                    vol.Optional(
                        "direction",
                        default=self.config_entry.options.get("direction", DEFAULT_DIRECTION)
                    ): vol.In(OPTIONS_DIRECTION),
                    
                    # Priorität
                    vol.Optional(
                        "priority",
                        default=self.config_entry.options.get("priority", DEFAULT_PRIORITY)
                    ): vol.In(OPTIONS_PRIORITY),
                    
                    # Wiederholungen
                    vol.Optional(
                        "repeat",
                        default=self.config_entry.options.get("repeat", DEFAULT_REPEAT)
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=10)),
                    
                    # Anzeigedauer
                    vol.Optional(
                        "duration",
                        default=self.config_entry.options.get("duration", DEFAULT_DURATION)
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
                    
                    # Transparenz
                    vol.Optional(
                        "transparency",
                        default=self.config_entry.options.get("transparency", DEFAULT_TRANSPARENCY)
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                }
            ),
        )
