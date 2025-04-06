from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Self

from homeassistant.components.light import (
    LightEntity,
    LightEntityDescription,
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    LightEntityFeature,
    ColorMode,
)
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .connector.model import ObegransadDeviceData
from .coordinator import ObegransadDataUpdateCoordinator
from .entity import ObegransadEntity
from .typing_helpers import ObegransadConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ObegransadLightEntityDescription(LightEntityDescription):
    value_fn: Callable[[ObegransadDeviceData], StateType]


SENSOR_TYPES: tuple[ObegransadLightEntityDescription, ...] = (
    ObegransadLightEntityDescription(
        key="light",
        translation_key="light",
        value_fn=lambda data: data.brightness > 0,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ObegransadConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        ObegransadLightEntity(coordinator, entry, description)
        for description in SENSOR_TYPES
    )


class ObegransadLightEntity(ObegransadEntity, LightEntity):
    entity_description: ObegransadLightEntityDescription

    def __init__(
        self: Self,
        coordinator: ObegransadDataUpdateCoordinator,
        entry: ObegransadConfigEntry,
        description: ObegransadLightEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, entry)
        host = entry.data[CONF_HOST]
        self.entity_description = description
        self._attr_unique_id = f"{host}_{description.key}"

    @property
    def is_on(self: Self) -> bool:
        """Return the value reported by the light."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def effect_list(self: Self) -> list[str]:
        return list(map(lambda p: p.name, self.coordinator.data.plugins))

    @property
    def effect(self: Self) -> str | None:
        """Return the current effect."""
        return next(
            filter(
                lambda p: p.id == self.coordinator.data.plugin,
                self.coordinator.data.plugins,
            )
        ).name

    @property
    def brightness(self: Self) -> str | None:
        """Return the current effect."""
        return self.coordinator.data.brightness

    async def async_turn_on(self: Self, **kwargs: Any) -> None:

        if ATTR_EFFECT in kwargs:
            effect = kwargs[ATTR_EFFECT]
            plugin_id = next(
                filter(lambda p: p.name == effect, self.coordinator.data.plugins)
            ).id
            await self.coordinator.obegransad_connector.set_plugin(plugin_id)

        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
            await self.coordinator.obegransad_connector.set_brightness(brightness)
        else:
            await self.coordinator.obegransad_connector.set_brightness(None)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self: Self, **kwargs: Any) -> None:
        await self.coordinator.obegransad_connector.set_brightness(0)
        await self.coordinator.async_request_refresh()

    @property
    def supported_features(self: Self) -> LightEntityFeature:
        """Flag supported features."""
        return LightEntityFeature.EFFECT

    @property
    def supported_color_modes(self: Self) -> set[ColorMode]:
        return {ColorMode.ONOFF, ColorMode.BRIGHTNESS}

    @property
    def use_device_name(self: Self) -> bool:
        return True
