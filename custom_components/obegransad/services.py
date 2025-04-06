import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall

from .const import (
    DOMAIN,
    ATTR_SCHEDULE,
    ATTR_PLUGIN_ID,
    ATTR_DURATION,
    SERVICE_SET_SCHEDULE,
    ATTR_MESSAGE_ID,
    SERVICE_CLEAR_STORAGE,
    SERVICE_REMOVE_MESSAGE,
)
from .coordinator import ObegransadDataUpdateCoordinator


def async_setup_services(
    hass: HomeAssistant, update_coordinator: ObegransadDataUpdateCoordinator
) -> None:
    async_setup_set_schedule_service(hass, update_coordinator)
    async_setup_remove_message_service(hass, update_coordinator)
    async_setup_clear_storage_service(hass, update_coordinator)


def async_setup_set_schedule_service(
    hass: HomeAssistant, update_coordinator: ObegransadDataUpdateCoordinator
) -> None:
    async def set_schedule(service: ServiceCall) -> None:
        await update_coordinator.obegransad_connector.set_schedule(
            service.data.get(ATTR_SCHEDULE)
        )
        await update_coordinator.async_request_refresh()

    schema = vol.Schema(
        {
            vol.Required(ATTR_SCHEDULE): vol.All(
                cv.ensure_list,
                [
                    vol.Schema(
                        {
                            vol.Required(ATTR_PLUGIN_ID): cv.positive_int,
                            vol.Optional(ATTR_DURATION): cv.positive_int,
                        }
                    )
                ],
            )
        }
    )

    hass.services.async_register(DOMAIN, SERVICE_SET_SCHEDULE, set_schedule, schema)


def async_setup_remove_message_service(
    hass: HomeAssistant, update_coordinator: ObegransadDataUpdateCoordinator
) -> None:
    async def remove_message(service: ServiceCall) -> None:
        await update_coordinator.obegransad_connector.remove_message(
            service.data.get(ATTR_MESSAGE_ID)
        )
        await update_coordinator.async_request_refresh()

    schema = vol.Schema({vol.Required(ATTR_MESSAGE_ID): cv.positive_int})
    hass.services.async_register(DOMAIN, SERVICE_REMOVE_MESSAGE, remove_message, schema)


def async_setup_clear_storage_service(
    hass: HomeAssistant, update_coordinator: ObegransadDataUpdateCoordinator
) -> None:
    async def remove_message(_service: ServiceCall) -> None:
        await update_coordinator.obegransad_connector.clear_storage()
        await update_coordinator.async_request_refresh()

    schema = vol.Schema({})
    hass.services.async_register(DOMAIN, SERVICE_CLEAR_STORAGE, remove_message, schema)
