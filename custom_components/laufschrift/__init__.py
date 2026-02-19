"""
Custom integration to control a Laufschrift.
"""
import asyncio
import logging

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    PLATFORMS,
    DEFAULT_PORT,
    SERVICE_LAUFSCHRIFT_SET_TEXT,
    SERVICE_LAUFSCHRIFT_SHUTDOWN,
    SERVICE_LAUFSCHRIFT_PAUSE,
    SERVICE_LAUFSCHRIFT_RESUME,
)

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
    name = entry.data.get("name")
    port = entry.data.get("port", DEFAULT_PORT)

    session = aiohttp.ClientSession()

    hass.data[DOMAIN][entry.entry_id] = {
        "host": host,
        "name": name,
        "port": port,
        "session": session,
    }

    # Helper-Funktion für API-Calls
    async def async_api_call(endpoint: str):
        """Make an API call to the Laufschrift."""
        url = f"http://{host}:{port}{endpoint}"
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error(f"API call failed: {url} - Status: {response.status}")
                    return False
                return True
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Could not connect to Laufschrift: {e}")
            return False

    # Service Handler
    async def async_set_text_service(call: ServiceCall):
        """Service call to set the text."""
        text = call.data.get("text", "")
        _LOGGER.debug(f"Setting text to {text}")
        await async_api_call(f"/text/{text}")

    async def async_shutdown_service(call: ServiceCall):
        """Service call to shutdown the Laufschrift."""
        _LOGGER.info("Shutting down the Laufschrift")
        await async_api_call("/shutdown")

    async def async_pause_service(call: ServiceCall):
        """Service call to pause the Laufschrift."""
        _LOGGER.info("Pausing the Laufschrift")
        await async_api_call("/pause")

    async def async_resume_service(call: ServiceCall):
        """Service call to resume the Laufschrift."""
        _LOGGER.info("Resuming the Laufschrift")
        await async_api_call("/resume")

    # Registriere die Services
    hass.services.async_register(
        DOMAIN, 
        SERVICE_LAUFSCHRIFT_SET_TEXT, 
        async_set_text_service,
        schema=vol.Schema({
            vol.Required("text"): cv.string,
        })
    )
    hass.services.async_register(DOMAIN, SERVICE_LAUFSCHRIFT_SHUTDOWN, async_shutdown_service)
    hass.services.async_register(DOMAIN, SERVICE_LAUFSCHRIFT_PAUSE, async_pause_service)
    hass.services.async_register(DOMAIN, SERVICE_LAUFSCHRIFT_RESUME, async_resume_service)

    # Speichere die api_call Funktion für andere Plattformen
    hass.data[DOMAIN][entry.entry_id]["async_api_call"] = async_api_call

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Session schließen
    session = hass.data[DOMAIN][entry.entry_id]["session"]
    await session.close()

    # Services entfernen
    hass.services.async_remove(DOMAIN, SERVICE_LAUFSCHRIFT_SET_TEXT)
    hass.services.async_remove(DOMAIN, SERVICE_LAUFSCHRIFT_SHUTDOWN)
    hass.services.async_remove(DOMAIN, SERVICE_LAUFSCHRIFT_PAUSE)
    hass.services.async_remove(DOMAIN, SERVICE_LAUFSCHRIFT_RESUME)

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