"""Device tracker platform for weenect."""
import logging
from typing import List

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, TRACKER_ADDED
from .entity import WeenectEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the weenect device_trackers."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    @callback
    def async_add_device_trackers(
        added: List[int],
    ) -> None:
        """Add device_trackers callback."""

        trackers: list = []
        for tracker_id in added:
            trackers.append(
                WeenectDeviceTracker(
                    coordinator,
                    tracker_id,
                )
            )

        async_add_entities(trackers, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        f"{config_entry.entry_id}_{TRACKER_ADDED}",
        async_add_device_trackers,
    )
    coordinator.unsub_dispatchers.append(unsub_dispatcher)
    if len(coordinator.data) > 0:
        async_add_device_trackers(coordinator.data.keys())


class WeenectDeviceTracker(WeenectEntity, TrackerEntity):
    """weenect device tracker."""

    @property
    def name(self):
        """Return the name of this tracker."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["name"]

    @property
    def latitude(self):
        """Return latitude value of the device."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["position"][0]["latitude"]

    @property
    def longitude(self):
        """Return longitude value of the device."""
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["position"][0]["longitude"]

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:paw"

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device.

        Value in meters.
        """
        if self.id in self.coordinator.data:
            return self.coordinator.data[self.id]["position"][0]["radius"]
