"""The kraken integration."""
import asyncio
from datetime import timedelta
import logging

import krakenex
import pykrakenapi
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_interval

from .const import DATA_UPDATED, DEFAULT_SCAN_INTERVAL, DOMAIN

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Optional(CONF_NAME, default=DOMAIN): cv.string})},
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the kraken component."""
    conf = config.get(DOMAIN)
    if conf:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, data=conf, context={"source": config_entries.SOURCE_IMPORT}
            )
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up kraken from a config entry."""
    kraken_data = KrakenData(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = kraken_data
    if not await kraken_data.async_setup():
        return False

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class KrakenData:
    """Define an object to hold sensor data."""

    def __init__(self, hass, config_entry):
        """Initialize."""
        self._hass = hass
        self._config_entry = config_entry
        self._api = pykrakenapi.KrakenAPI(krakenex.API(), retry=0)
        self._unsub_timer = None
        self.tradable_asset_pairs = None
        self.data = None
        self.available = False

    async def async_update(self):
        """Get the latest data from the Kraken.com REST API."""
        try:
            self.data = await self._hass.async_add_executor_job(self._get_kraken_data)
            self.available = True
            _LOGGER.debug("Kraken.com data updated")
            async_dispatcher_send(self._hass, DATA_UPDATED)
        except pykrakenapi.pykrakenapi.KrakenAPIError as error:
            if "Unknown asset pair" in str(error):
                _LOGGER.info(
                    "Kraken.com reported an unknown asset pair. Refreshing list of tradable asset pairs."
                )
                await self._async_refresh_tradable_asset_pairs()
                await self.async_update()
            else:
                _LOGGER.error("Unable to fetch data from Kraken.com: %s", error)
                self.available = False

    def _get_kraken_data(self) -> dict:
        prepared_pairs = self._get_prepared_asset_pairs()
        ticker_df = self._api.get_ticker_information(prepared_pairs)
        # Rename columns to their full name
        ticker_df.columns = [
            "ask",
            "bid",
            "last_trade_closed",
            "volume",
            "volume_weighted_average",
            "number_of_trades",
            "low",
            "high",
            "opening_price",
        ]
        response_dict = ticker_df.transpose().to_dict()
        return response_dict

    def _get_tradable_asset_pairs(self) -> list:
        tradable_asset_pairs = []
        asset_pairs_df = self._api.get_tradable_asset_pairs()
        for pair in zip(asset_pairs_df.index.values, asset_pairs_df["wsname"]):
            try:
                if ".d" not in pair[0]:  # Remove strange duplicates
                    tradable_asset_pairs.append([pair[0], pair[1].split("/")])
            except AttributeError:
                # Ignore NaN
                pass
        return tradable_asset_pairs

    def _get_prepared_asset_pairs(self):
        return ",".join(pair[0] for pair in self.tradable_asset_pairs)

    async def _async_refresh_tradable_asset_pairs(self):
        self.tradable_asset_pairs = await self._hass.async_add_executor_job(
            self._get_tradable_asset_pairs
        )

    async def async_setup(self):
        """Set up the Kraken integration."""
        await self._async_refresh_tradable_asset_pairs()
        self.add_options()
        self.set_scan_interval(self._config_entry.options[CONF_SCAN_INTERVAL])
        self._config_entry.add_update_listener(self.async_options_updated)

        self._hass.async_create_task(
            self._hass.config_entries.async_forward_entry_setup(
                self._config_entry, "sensor"
            )
        )
        return True

    def add_options(self):
        """Add options for Kraken integration."""
        if not self._config_entry.options:
            options = {CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL}
            self._hass.config_entries.async_update_entry(
                self._config_entry, options=options
            )

    def set_scan_interval(self, scan_interval):
        """Update scan interval."""

        async def refresh(event_time):
            """Get the latest data from Kraken api."""
            await self.async_update()

        if self._unsub_timer is not None:
            self._unsub_timer()
        self._unsub_timer = async_track_time_interval(
            self._hass, refresh, timedelta(seconds=scan_interval)
        )

    @staticmethod
    async def async_options_updated(hass, entry):
        """Triggered by config entry options updates."""
        hass.data[DOMAIN][entry.entry_id].set_scan_interval(
            entry.options[CONF_SCAN_INTERVAL]
        )
