from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Mapping, Self

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import CONF_HOST, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connector.model import ObegransadDeviceData
from .coordinator import ObegransadDataUpdateCoordinator
from .entity import ObegransadEntity
from .typing_helpers import ObegransadConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ObegransadSwitchEntityDescription(SwitchEntityDescription):
    value_fn: Callable[[ObegransadDeviceData], bool]
    attrs_fn: Callable[[ObegransadDeviceData], dict] | None = None


SENSOR_TYPES: tuple[ObegransadSwitchEntityDescription, ...] = (
    ObegransadSwitchEntityDescription(
        key="schedule",
        translation_key="schedule",
        value_fn=lambda data: data.schedule_active,
        attrs_fn=lambda data: {"schedule": data.schedule},
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ObegransadConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        ObegransadSwitchEntity(coordinator, entry, description)
        for description in SENSOR_TYPES
    )


class ObegransadSwitchEntity(ObegransadEntity, SwitchEntity):
    entity_description: ObegransadSwitchEntityDescription

    def __init__(
        self: Self,
        coordinator: ObegransadDataUpdateCoordinator,
        entry: ObegransadConfigEntry,
        description: ObegransadSwitchEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, entry)
        host = entry.data[CONF_HOST]
        self.entity_description = description
        self._attr_unique_id = f"{host}_{description.key}"

    @property
    def is_on(self: Self) -> bool:
        """Return the value reported by the switch."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_turn_on(self: Self, **kwargs: Any) -> None:
        await self.coordinator.obegransad_connector.start_schedule()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self: Self, **kwargs: Any) -> None:
        await self.coordinator.obegransad_connector.stop_schedule()
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self: Self) -> Mapping[str, Any] | None:
        if self.entity_description.attrs_fn is None:
            return {}
        return self.entity_description.attrs_fn(self.coordinator.data)
