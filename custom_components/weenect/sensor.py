"""Sensor platform for weenect."""
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOCATION_SENSOR_TYPES, SENSOR_TYPES, TRACKER_ADDED
from .entity import WeenectEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the weenect sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    @callback
    def async_add_sensors(
        added: List[int],
    ) -> None:
        """Add sensors callback."""

        sensors: list = []
        for tracker_id in added:
            for sensor_type in SENSOR_TYPES:
                sensors.append(WeenectSensor(coordinator, tracker_id, sensor_type))
            for sensor_type in LOCATION_SENSOR_TYPES:
                sensors.append(
                    WeenectLocationSensor(coordinator, tracker_id, sensor_type)
                )

        async_add_entities(sensors, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        f"{entry.entry_id}_{TRACKER_ADDED}",
        async_add_sensors,
    )
    coordinator.unsub_dispatchers.append(unsub_dispatcher)
    if len(coordinator.data) > 0:
        async_add_sensors(coordinator.data.keys())


class WeenectSensorBase(WeenectEntity):
    """weenect Sensor Base."""

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
        self._unit_of_measurement = sensor_type["unit_of_measurement"]

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
    def device_class(self):
        """Device class of this entity."""
        return self._device_class

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return self._enabled

    @property
    def unit_of_measurement(self):
        """Return the units of measurement."""
        return self._unit_of_measurement


class WeenectSensor(WeenectSensorBase):
    """weenect sensor for general informatio."""

    @property
    def state(self):
        """Return the state of the resources if it has been received yet."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id][self._value_name]


class WeenectLocationSensor(WeenectSensorBase):
    """weenect sensor for location informatio."""

    @property
    def state(self):
        """Return the state of the resources if it has been received yet."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["position"][0][self._value_name]
