"""Adds config flow for Laufschrift."""
import logging
import aiohttp

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LaufschriftConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Laufschrift."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}
        if user_input is not None:
            try:
                # Ersetze dies durch eine tatsächliche Verbindung zur Laufschrift
                info = await self._test_connect(user_input[CONF_HOST])
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
            )

    async def _test_connect(self, host):
        """Test connection to the Laufschrift."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{host}:5000/") as response:
                    if response.status == 200:
                        return True
                    else:
                        return False
        except:
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle options flow."""
        return LaufschriftOptionsFlow(config_entry)


class LaufschriftOptionsFlow(config_entries.OptionsFlow):
    """Options flow for Laufschrift."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        brightness_options = ["30", "80", "130", "180", "230", "255"]
        speed_options = ["1", "2", "3", "4", "5"]

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("brightness", default=self.config_entry.options.get("brightness", "230")): vol.In(brightness_options),
                    vol.Optional("speed", default=self.config_entry.options.get("speed", "3")): vol.In(speed_options),
                }
            ),
        )
