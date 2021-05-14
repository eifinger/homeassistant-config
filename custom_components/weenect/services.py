"""weenect services."""
import logging

from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN

DOMAIN_SERVICES = f"{DOMAIN}_services"

TRACKER_ID = "tracker_id"
UPDATE_INTERVAL = "update_interval"

SERVICE_SET_UPDATE_INTERVAL = "set_update_interval"
SERVICE_SET_UPDATE_INTERVAL_SCHEMA = vol.Schema(
    {
        vol.Required(TRACKER_ID): cv.string,
        vol.Optional(UPDATE_INTERVAL, default="30M"): cv.string,
    }
)

SERVICE_ACTIVATE_SUPER_LIVE = "activate_super_live"
SERVICE_REFRESH_LOCATION = "refresh_location"
SERVICE_RING = "ring"
SERVICE_VIBRATE = "vibrate"
SERVICE_SCHEMA = vol.Schema({vol.Required(TRACKER_ID): cv.string})

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_services(hass):
    """Set up services for weenect integration."""
    if hass.data.get(DOMAIN_SERVICES, False):
        return

    hass.data[DOMAIN_SERVICES] = True

    async def async_call_service(service_call):
        """Call correct weenect service."""
        service = service_call.service
        service_data = service_call.data

        if service == SERVICE_SET_UPDATE_INTERVAL:
            await async_set_update_interval(hass, service_data)
        if service == SERVICE_ACTIVATE_SUPER_LIVE:
            await async_activate_super_live(hass, service_data)
        if service == SERVICE_REFRESH_LOCATION:
            await async_refresh_location(hass, service_data)
        if service == SERVICE_RING:
            await async_ring(hass, service_data)
        if service == SERVICE_VIBRATE:
            await async_vibrate(hass, service_data)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_UPDATE_INTERVAL,
        async_call_service,
        schema=SERVICE_SET_UPDATE_INTERVAL_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_ACTIVATE_SUPER_LIVE,
        async_call_service,
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_LOCATION,
        async_call_service,
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_RING,
        async_call_service,
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_VIBRATE,
        async_call_service,
        schema=SERVICE_SCHEMA,
    )


async def async_unload_services(hass):
    """Unload weenect services."""
    if not hass.data.get(DOMAIN_SERVICES):
        return

    hass.data[DOMAIN_SERVICES] = False

    hass.services.async_remove(DOMAIN, SERVICE_SET_UPDATE_INTERVAL)
    hass.services.async_remove(DOMAIN, SERVICE_ACTIVATE_SUPER_LIVE)
    hass.services.async_remove(DOMAIN, SERVICE_REFRESH_LOCATION)
    hass.services.async_remove(DOMAIN, SERVICE_RING)
    hass.services.async_remove(DOMAIN, SERVICE_VIBRATE)


async def async_set_update_interval(hass, data):
    """Set the update interval for this tracker id."""

    tracker_id = int(data[TRACKER_ID])
    update_interval = data[UPDATE_INTERVAL]

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.set_update_interval(
                tracker_id, update_interval
            )
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_activate_super_live(hass, data):
    """Activate the super live mode for this tracker id"""

    tracker_id = int(data[TRACKER_ID])

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.activate_super_live(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_refresh_location(hass, data):
    """Request a position refresh for this tracker id"""

    tracker_id = int(data[TRACKER_ID])

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.refresh_location(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_ring(hass, data):
    """Send a ring command for this tracker id"""

    tracker_id = int(data[TRACKER_ID])

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.ring(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )


async def async_vibrate(hass, data):
    """Send a vibrate command for this tracker id"""

    tracker_id = int(data[TRACKER_ID])

    for config_entry in hass.data[DOMAIN]:
        if tracker_id in hass.data[DOMAIN][config_entry].data.keys():
            await hass.data[DOMAIN][config_entry].client.vibrate(tracker_id)
            return
    _LOGGER.warning(
        "Could not find a registered integration for tracker with id: %s", tracker_id
    )
