"""Adds config flow for weenect."""
import logging

from aioweenect import AioWeenect
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol

from .const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class WeenectFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for weenect."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        entries = self._async_current_entries()
        for entry in entries:
            if (
                entry.data[CONF_USERNAME] == user_input[CONF_USERNAME]
                and entry.data[CONF_PASSWORD] == user_input[CONF_PASSWORD]
            ):
                return self.async_abort(reason="already_configured")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )
            self._errors["base"] = "auth"

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password) -> bool:
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = AioWeenect(username=username, password=password, session=session)
            await client.login()
            return True
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.debug(exception)
        return False
