from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Mapping, Any, Self

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import CONF_HOST, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .connector.model import ObegransadDeviceData
from .coordinator import ObegransadDataUpdateCoordinator
from .entity import ObegransadEntity
from .typing_helpers import ObegransadConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ObegransadSensorEntityDescription(SensorEntityDescription):
    value_fn: Callable[[ObegransadDeviceData], StateType]
    attrs_fn: Callable[[ObegransadDeviceData], dict] | None = None


SENSOR_TYPES: tuple[ObegransadSensorEntityDescription, ...] = (
    ObegransadSensorEntityDescription(
        key="rows",
        translation_key="rows",
        suggested_display_precision=0,
        value_fn=lambda data: data.rows,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="columns",
        translation_key="columns",
        suggested_display_precision=0,
        value_fn=lambda data: data.columns,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="status",
        translation_key="status",
        suggested_display_precision=0,
        value_fn=lambda data: data.status,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="plugin",
        translation_key="plugin",
        suggested_display_precision=0,
        value_fn=lambda data: data.plugin,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="rotation",
        translation_key="rotation",
        suggested_display_precision=0,
        value_fn=lambda data: data.rotation,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="brightness",
        translation_key="brightness",
        suggested_display_precision=0,
        value_fn=lambda data: data.brightness,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    ObegransadSensorEntityDescription(
        key="schedule",
        translation_key="schedule",
        suggested_display_precision=0,
        value_fn=lambda data: len(data.schedule),
        attrs_fn=lambda data: {"schedule": data.schedule},
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ObegransadSensorEntityDescription(
        key="plugins",
        translation_key="plugins",
        suggested_display_precision=0,
        value_fn=lambda data: len(data.plugins),
        attrs_fn=lambda data: {"plugins": data.plugins},
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ObegransadConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        ObegransadSensorEntity(coordinator, entry, description)
        for description in SENSOR_TYPES
    )


class ObegransadSensorEntity(ObegransadEntity, SensorEntity):
    entity_description: ObegransadSensorEntityDescription

    def __init__(
        self: Self,
        coordinator: ObegransadDataUpdateCoordinator,
        entry: ObegransadConfigEntry,
        description: ObegransadSensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, entry)
        host = entry.data[CONF_HOST]
        self.entity_description = description
        self._attr_unique_id = f"{host}_{description.key}"

    @property
    def native_value(self: Self) -> StateType:
        """Return the value reported by the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self: Self) -> Mapping[str, Any] | None:
        if self.entity_description.attrs_fn is None:
            return {}
        return self.entity_description.attrs_fn(self.coordinator.data)
