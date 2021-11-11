"""weenect services."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN

DOMAIN_SERVICES = f"{DOMAIN}_services"

UPDATE_INTERVAL = "update_interval"

SERVICE_SET_UPDATE_INTERVAL = "set_update_interval"
SERVICE_SET_UPDATE_INTERVAL_SCHEMA = cv.make_entity_service_schema(
    {
        vol.Optional(UPDATE_INTERVAL, default="30M"): cv.string,
    }
)

SERVICE_ACTIVATE_SUPER_LIVE = "activate_super_live"
SERVICE_REFRESH_LOCATION = "refresh_location"
SERVICE_RING = "ring"
SERVICE_VIBRATE = "vibrate"
SERVICE_SCHEMA = cv.make_entity_service_schema({})

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_set_update_interval(
    hass: HomeAssistant, tracker_id: int, update_interval: str
):
    """Set the update interval for this tracker id."""

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.set_update_interval(
                tracker_id, update_interval
            )
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_activate_super_live(hass: HomeAssistant, tracker_id: int):
    """Activate the super live mode for this tracker id"""

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.activate_super_live(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_refresh_location(hass: HomeAssistant, tracker_id: int):
    """Request a position refresh for this tracker id"""

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.refresh_location(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_ring(hass: HomeAssistant, tracker_id: int):
    """Send a ring command for this tracker id"""

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.ring(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_vibrate(hass: HomeAssistant, tracker_id: int):
    """Send a vibrate command for this tracker id"""

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.vibrate(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )
