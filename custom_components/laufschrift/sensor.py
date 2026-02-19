"""Platform for sensor integration."""
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.info("Setting up sensor platform")
    host = config_entry.data.get("host")
    port = config_entry.data.get("port", DEFAULT_PORT)
    name = config_entry.data.get("name")

    async_add_entities([
        LaufschriftTextSensor(host, port, name),
        LaufschriftBrightnessSensor(host, port, name),
        LaufschriftSpeedSensor(host, port, name),
    ])


# =============================================================================
# Basis-Klasse für alle Sensor-Entitäten
# =============================================================================

class LaufschriftSensorBase(SensorEntity):
    """Base class for Laufschrift sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        host: str,
        port: int,
        device_name: str,
        sensor_name: str,
        icon: str,
    ) -> None:
        """Initialize the sensor."""
        self._host = host
        self._port = port
        self._device_name = device_name
        self._attr_available = True
        self._value = None
        self._attr_unique_id = f"laufschrift_{host}_{device_name}_{sensor_name.lower().replace(' ', '_')}_sensor"
        self._attr_name = f"{device_name} {sensor_name}"
        self._attr_icon = icon

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._value


# =============================================================================
# Text Sensor
# =============================================================================

class LaufschriftTextSensor(LaufschriftSensorBase):
    """Representation of the Laufschrift text sensor."""

    def __init__(self, host: str, port: int, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            host, port, name,
            sensor_name="Aktueller Text",
            icon="mdi:text",
        )
        self._value = "Kein Text"


# =============================================================================
# Helligkeit Sensor
# =============================================================================

class LaufschriftBrightnessSensor(LaufschriftSensorBase):
    """Representation of the Laufschrift brightness sensor."""

    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host: str, port: int, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            host, port, name,
            sensor_name="Aktuelle Helligkeit",
            icon="mdi:brightness-6",
        )
        self._value = 230

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return None


# =============================================================================
# Geschwindigkeit Sensor
# =============================================================================

class LaufschriftSpeedSensor(LaufschriftSensorBase):
    """Representation of the Laufschrift speed sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host: str, port: int, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            host, port, name,
            sensor_name="Aktuelle Geschwindigkeit",
            icon="mdi:speedometer",
        )
        self._value = 3