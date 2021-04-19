"""Binary_sensor platform for weenect."""
import logging
from typing import Any, Dict, List

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import BINARY_SENSOR_TYPES, DOMAIN, TRACKER_ADDED
from .entity import WeenectEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the weenect binary_sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    @callback
    def async_add_binary_sensors(
        added: List[int],
    ) -> None:
        """Add binary_sensors callback."""

        sensors: list = []
        for tracker_id in added:
            for sensor_type in BINARY_SENSOR_TYPES:
                sensors.append(
                    WeenectBinarySensor(coordinator, tracker_id, sensor_type)
                )

        async_add_entities(sensors, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        f"{config_entry.entry_id}_{TRACKER_ADDED}",
        async_add_binary_sensors,
    )
    coordinator.unsub_dispatchers.append(unsub_dispatcher)
    if len(coordinator.data) > 0:
        async_add_binary_sensors(coordinator.data.keys())


class WeenectBinarySensor(WeenectEntity, BinarySensorEntity):
    """weenect binary_sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        tracker_id: str,
        sensor_type: Dict[str, Any],
    ):
        super().__init__(coordinator, tracker_id)
        self._device_class = sensor_type["device_class"]
        self._value_name = sensor_type["value_name"]
        self._enabled = sensor_type["enabled"]
        self._name = sensor_type["name"]

    @property
    def name(self):
        """Return the name of this tracker."""
        if self.id in self.coordinator.data:
            return f"{self.coordinator.data[self.id]['name']} {self._name}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.id}_{self._value_name}"

    @property
    def is_on(self):
        """Return True if the binary sensor is on."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["position"][0][self._value_name]

    @property
    def device_class(self):
        """Device class of this entity."""
        return self._device_class

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return self._enabled
