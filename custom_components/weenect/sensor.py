"""Sensor platform for weenect."""
import logging
from typing import Any, Dict, List

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, SENSOR_TYPES, TRACKER_ADDED
from .entity import WeenectEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the weenect sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    @callback
    def async_add_sensors(
        added: List[int],
    ) -> None:
        """Add sensors callback."""

        sensors: list = []
        for tracker_id in added:
            for sensor_type in SENSOR_TYPES:
                sensors.append(WeenectSensor(coordinator, tracker_id, sensor_type))

        async_add_entities(sensors, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        f"{config_entry.entry_id}_{TRACKER_ADDED}",
        async_add_sensors,
    )
    coordinator.unsub_dispatchers.append(unsub_dispatcher)
    if len(coordinator.data) > 0:
        async_add_sensors(coordinator.data.keys())


class WeenectSensor(WeenectEntity):
    """weenect sensor."""

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
    def state(self):
        """Return the state of the resources if it has been received yet."""
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
