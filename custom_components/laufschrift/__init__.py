"""
Custom integration to control a Laufschrift.
"""
import asyncio
import logging

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, PLATFORMS, SERVICE_LAUFSCHRIFT_SET_TEXT, SERVICE_LAUFSCHRIFT_SHUTDOWN

_LOGGER: logging.Logger = logging.getLogger(__package__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required("host"): cv.string,
        })
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up this integration using YAML is not allowed."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    host = entry.data.get("host")
    name = entry.data.get("name")  # Hole den Namen aus der ConfigEntry

    session = aiohttp.ClientSession()

    hass.data[DOMAIN][entry.entry_id] = {
        "host": host,
        "name": name,  # Speichere den Namen in den Daten
        "session": session,
    }

    # Definiere die Service-Handler
    async def async_set_text_service(call: ServiceCall):
        """Service call to set the text."""
        text = call.data.get("text", "")
        _LOGGER.debug(f"Setting text to {text}")
        await async_set_value(hass, entry, "text", text)

    async def async_shutdown_service(call: ServiceCall):
        """Service call to shutdown the Laufschrift."""
        _LOGGER.info("Shutting down the Laufschrift")
        await async_set_value(hass, entry, "shutdown", True)

    async def async_set_value(hass: HomeAssistant, entry: ConfigEntry, parameter: str, value):
        """Set a value on the Laufschrift."""
        host = entry.data.get("host")
        session = hass.data[DOMAIN][entry.entry_id]["session"]
        try:
            if parameter == "text":
                url = f"http://{host}:5000/text/{value}"
            elif parameter == "shutdown":
                url = f"http://{host}:5000/shutdown"
            else:
                _LOGGER.error(f"Invalid parameter: {parameter}")
                return

            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error(f"Error setting {parameter}: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")

    # Registriere die Services
    hass.services.async_register(DOMAIN, SERVICE_LAUFSCHRIFT_SET_TEXT, async_set_text_service)
    hass.services.async_register(DOMAIN, SERVICE_LAUFSCHRIFT_SHUTDOWN, async_shutdown_service)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    session = hass.data[DOMAIN][entry.entry_id]["session"]
    await session.close()

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok