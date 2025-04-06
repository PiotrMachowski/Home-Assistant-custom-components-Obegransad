from __future__ import annotations

import logging
from typing import Any, Self

import voluptuous as vol
from aiohttp import ClientError
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .connector import ObegransadConnector
from .connector.exceptions import ObegransadException
from .const import DOMAIN, NAME

_LOGGER = logging.getLogger(__name__)


class ObegransadFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self: Self) -> None:
        self._token = None
        self._all_devices = []

    async def async_step_user(
        self: Self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

        if user_input is not None:
            client_session = async_get_clientsession(self.hass)
            host = user_input[CONF_HOST]
            obegransad_connector = ObegransadConnector(client_session, host)
            data = None
            try:
                data = await obegransad_connector.get_data()
            except (ClientError, TimeoutError, ObegransadException) as e:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            is_valid = data is not None and data.rows == 16
            if is_valid:
                self._token = self._token
                return self.async_create_entry(title=NAME, data={CONF_HOST: host})
            else:
                errors[CONF_HOST] = "invalid_host"

        schema: vol.Schema = vol.Schema({vol.Required(CONF_HOST): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
