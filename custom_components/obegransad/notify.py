"""Support for Obegransad notification service."""

from __future__ import annotations

from typing import Any, Self

from homeassistant.components.notify import ATTR_DATA, BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    ATTR_GRAPH,
    ATTR_MIN_Y,
    ATTR_MAX_Y,
    ATTR_REPEAT,
    ATTR_MESSAGE_ID,
    ATTR_DELAY,
    ATTR_CONFIG_ENTRY_ID,
)
from .typing_helpers import ObegransadConfigEntry, ObegransadRuntimeData


async def async_get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> BaseNotificationService | None:
    """Return the notify service."""

    if discovery_info is None:
        return None

    config_entry = hass.config_entries.async_get_entry(
        discovery_info[ATTR_CONFIG_ENTRY_ID]
    )
    assert config_entry is not None

    return ObegransadNotificationService(config_entry)


class ObegransadNotificationService(BaseNotificationService):
    """Implement the notification service for Obegransad display."""

    def __init__(self: Self, entry: ObegransadConfigEntry) -> None:
        """Initialize the service."""
        self._entry = entry

    async def async_send_message(self: Self, message: str = "", **kwargs: Any) -> None:
        """Send a message to the Obegransad display."""
        runtime_data: ObegransadRuntimeData = self._entry.runtime_data
        connector = runtime_data.coordinator.obegransad_connector

        data = kwargs[ATTR_DATA] or {}
        text = message
        graph = data.get(ATTR_GRAPH)
        min_y = data.get(ATTR_MIN_Y)
        max_y = data.get(ATTR_MAX_Y)
        repeat = data.get(ATTR_REPEAT)
        message_id = data.get(ATTR_MESSAGE_ID)
        delay = data.get(ATTR_DELAY)

        await connector.display_message(
            text, graph, min_y, max_y, repeat, message_id, delay
        )
