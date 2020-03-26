"""The kraken integration."""
from datetime import timedelta
import logging

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DATA_UPDATED, DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add kraken entities from a config_entry."""
    kraken_data = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []

    for asset_pair in kraken_data.tradable_asset_pairs:
        sensors.append(
            KrakenSensor(
                kraken_data, config_entry.data["name"], asset_pair[0], asset_pair[1]
            )
        )
    async_add_entities(sensors, True)


class KrakenSensor(Entity):
    """Define a Kraken sensor."""

    def __init__(self, kraken_data, name, pair_name, pair):
        """Initialize."""
        self._kraken_data = kraken_data
        self._pair_name = pair_name
        self._unit_of_measurement = pair[1]
        self._name = "_".join([name, *pair])
        self._state = None
        self._available = True
        self._async_remove_dispatcher = None
        self._attrs = {
            "ask": None,
            "ask_volume": None,
            "bid": None,
            "bid_volume": None,
            "volume_today": None,
            "volume_last_24h": None,
            "volume_weighted_average_today": None,
            "volume_weighted_average_last_24h": None,
            "number_of_trades_today": None,
            "number_of_trades_last_24h": None,
            "low_today": None,
            "low_last_24h": None,
            "high_today": None,
            "high_last_24h": None,
            "opening_price_today": None,
        }

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def unique_id(self):
        """Set unique_id for sensor."""
        return self._name

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attrs

    @property
    def icon(self):
        """Return the icon."""
        if self._name[-3:] == "EUR":
            return "mdi:currency-eur"
        if self._name[-3:] == "USD":
            return "mdi:currency-usd"
        if self._name[-3:] == "XBT":
            return "mdi:currency-btc"
        return "mdi:coin"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        if self._available:
            return self._kraken_data.available
        return self._available

    @property
    def should_poll(self):
        """Return the polling requirement for this sensor."""
        return False

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return True

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        self._async_remove_dispatcher = async_dispatcher_connect(
            self.hass, DATA_UPDATED, self._schedule_immediate_update
        )

    async def async_will_remove_from_hass(self):
        """Unsubscribe from updates."""
        if self._async_remove_dispatcher:
            self._async_remove_dispatcher()

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        """Get the latest data from kraken.com."""
        if self._kraken_data.data is not None:
            try:
                self._state = self._kraken_data.data[self._pair_name][
                    "last_trade_closed"
                ][0]
                self._attrs["ask"] = self._kraken_data.data[self._pair_name]["ask"][0]
                self._attrs["ask_volume"] = self._kraken_data.data[self._pair_name][
                    "ask"
                ][1]
                self._attrs["bid"] = self._kraken_data.data[self._pair_name]["bid"][0]
                self._attrs["bid_volume"] = self._kraken_data.data[self._pair_name][
                    "bid"
                ][1]
                self._attrs["volume_today"] = self._kraken_data.data[self._pair_name][
                    "volume"
                ][0]
                self._attrs["volume_last_24h"] = self._kraken_data.data[
                    self._pair_name
                ]["volume"][1]
                self._attrs["volume_weighted_average_today"] = self._kraken_data.data[
                    self._pair_name
                ]["volume_weighted_average"][0]
                self._attrs[
                    "volume_weighted_average_last_24h"
                ] = self._kraken_data.data[self._pair_name]["volume_weighted_average"][
                    1
                ]
                self._attrs["number_of_trades_today"] = str(
                    self._kraken_data.data[self._pair_name]["number_of_trades"][0]
                )
                self._attrs["number_of_trades_last_24h"] = str(
                    self._kraken_data.data[self._pair_name]["number_of_trades"][1]
                )
                self._attrs["low_today"] = self._kraken_data.data[self._pair_name][
                    "low"
                ][0]
                self._attrs["low_last_24h"] = self._kraken_data.data[self._pair_name][
                    "low"
                ][1]
                self._attrs["high_today"] = self._kraken_data.data[self._pair_name][
                    "high"
                ][0]
                self._attrs["high_last_24h"] = self._kraken_data.data[self._pair_name][
                    "high"
                ][1]
                self._attrs["opening_price_today"] = self._kraken_data.data[
                    self._pair_name
                ]["opening_price"]
            except KeyError:
                if self._available:
                    _LOGGER.warning("Asset Pair %s is no longer available", self._name)
                self._available = False
