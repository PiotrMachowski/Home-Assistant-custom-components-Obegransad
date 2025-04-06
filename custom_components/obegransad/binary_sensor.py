from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Mapping, Any, Self

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import CONF_HOST, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connector.model import ObegransadDeviceData
from .coordinator import ObegransadDataUpdateCoordinator
from .entity import ObegransadEntity
from .typing_helpers import ObegransadConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ObegransadBinarySensorEntityDescription(BinarySensorEntityDescription):
    value_fn: Callable[[ObegransadDeviceData], bool]
    attrs_fn: Callable[[ObegransadDeviceData], dict] | None = None


SENSOR_TYPES: tuple[ObegransadBinarySensorEntityDescription, ...] = (
    ObegransadBinarySensorEntityDescription(
        key="schedule_active",
        translation_key="schedule_active",
        value_fn=lambda data: data.schedule_active,
        attrs_fn=lambda data: {"schedule": data.schedule},
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ObegransadConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        ObegransadBinarySensorEntity(coordinator, entry, description)
        for description in SENSOR_TYPES
    )


class ObegransadBinarySensorEntity(ObegransadEntity, BinarySensorEntity):
    entity_description: ObegransadBinarySensorEntityDescription

    def __init__(
        self: Self,
        coordinator: ObegransadDataUpdateCoordinator,
        entry: ObegransadConfigEntry,
        description: ObegransadBinarySensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, entry)
        host = entry.data[CONF_HOST]
        self.entity_description = description
        self._attr_unique_id = f"{host}_{description.key}"

    @property
    def is_on(self: Self) -> bool:
        """Return the value reported by the binary sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self: Self) -> Mapping[str, Any] | None:
        if self.entity_description.attrs_fn is None:
            return {}
        return self.entity_description.attrs_fn(self.coordinator.data)
