"""
Custom integration to integrate weenect with Home Assistant.

For more details about this integration, please refer to
https://github.com/eifinger/hass-weenect
"""
import asyncio
from datetime import timedelta
import logging
from typing import Any

from aioweenect import AioWeenect
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_PASSWORD,
    CONF_UPDATE_RATE,
    CONF_USERNAME,
    DEFAULT_UPDATE_RATE,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
    TRACKER_ADDED,
)
from .services import async_setup_services, async_unload_services

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        await async_setup_services(hass)
        _LOGGER.info(STARTUP_MESSAGE)

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = async_get_clientsession(hass)
    client = AioWeenect(username=username, password=password, session=session)

    coordinator = WeenectDataUpdateCoordinator(hass, config_entry=entry, client=client)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.add_update_listener(async_reload_entry)
    return True


class WeenectDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, client: AioWeenect
    ) -> None:
        """Initialize."""
        if CONF_UPDATE_RATE in config_entry.options:
            update_interval = timedelta(seconds=config_entry.options[CONF_UPDATE_RATE])
        else:
            update_interval = timedelta(seconds=DEFAULT_UPDATE_RATE)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.client = client
        self.config_entry = config_entry
        self.unsub_dispatchers = []
        self.data = {}
        self.add_options()

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.client.get_trackers()
            data = self.transform_data(data)
            self._detect_added_and_removed_trackers(data)
            return data
        except Exception as exception:
            raise UpdateFailed(exception) from exception

    def _detect_added_and_removed_trackers(self, data: Any):
        """Detect if trackers were added or removed."""
        added = set(data.keys()) - set(self.data.keys())
        async_dispatcher_send(
            self.hass, f"{self.config_entry.entry_id}_{TRACKER_ADDED}", added
        )

    @staticmethod
    def transform_data(data: Any):
        """Extract trackers from list and put them in a dict by tracker id."""
        result = {}
        for tracker in data["items"]:
            result[tracker["id"]] = tracker
        return result

    def add_options(self) -> None:
        """Add options for weenect integration."""
        if not self.config_entry.options:
            options = {
                CONF_UPDATE_RATE: DEFAULT_UPDATE_RATE,
            }
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=options
            )
        else:
            options = dict(self.config_entry.options)
            if CONF_UPDATE_RATE not in self.config_entry.options:
                options[CONF_UPDATE_RATE] = DEFAULT_UPDATE_RATE
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=options
            )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    for unsub_dispatcher in hass.data[DOMAIN][entry.entry_id].unsub_dispatchers:
        unsub_dispatcher()
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    # If there is no instance of this integration registered anymore
    if not hass.data[DOMAIN]:
        await async_unload_services(hass)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
