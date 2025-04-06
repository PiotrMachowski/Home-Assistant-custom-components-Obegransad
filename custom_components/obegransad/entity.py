from typing import Self

from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ObegransadDataUpdateCoordinator
from .typing_helpers import ObegransadConfigEntry


class ObegransadEntity(CoordinatorEntity[ObegransadDataUpdateCoordinator]):
    _attr_has_entity_name = True

    def __init__(
        self: Self,
        coordinator: ObegransadDataUpdateCoordinator,
        config_entry: ObegransadConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self.coordinator = coordinator

    @property
    def device_info(self: Self) -> DeviceInfo:
        host = self._config_entry.data[CONF_HOST]
        return {
            "identifiers": {(DOMAIN, host)},
            "configuration_url": f"http://{host}/",
        }
