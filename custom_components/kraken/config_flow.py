"""Config flow for kraken integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class KrakenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for kraken."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KrakenOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            if any(
                user_input["name"] == entry.data["name"]
                for entry in self._async_current_entries()
            ):
                return self.async_abort(reason="already_configured")

            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("name", default=DOMAIN): str}),
            errors={},
        )

    async def async_step_import(self, import_config):
        """Import from Kraken sensor config."""
        return await self.async_step_user(user_input=import_config)


class KrakenOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Kraken client options."""

    def __init__(self, config_entry):
        """Initialize Kraken options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the Kraken options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=self.config_entry.options.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
            ): int
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
