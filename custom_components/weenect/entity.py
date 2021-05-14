"""weenect class"""
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import ATTRIBUTION, DOMAIN, NAME


class WeenectEntity(CoordinatorEntity):
    """Base entity for weenect."""

    def __init__(self, coordinator: DataUpdateCoordinator, tracker_id: str):
        super().__init__(coordinator)
        self.id = tracker_id

    @property
    def device_name(self):
        """Return the name of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["name"]

    @property
    def imei(self):
        """Return the imei of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["imei"]

    @property
    def sim(self):
        """Return the sim of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["sim"]

    @property
    def tracker_type(self):
        """Return the type of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["type"]

    @property
    def firmware(self):
        """Return the firmware of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["firmware"]

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.id)},
            "name": self.device_name,
            "model": self.tracker_type,
            "manufacturer": NAME,
            "sw_version": self.firmware,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": self.id,
            "sim": self.sim,
            "imei": self.imei,
        }
