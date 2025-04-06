from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from .coordinator import ObegransadDataUpdateCoordinator


@dataclass
class ObegransadRuntimeData:
    coordinator: ObegransadDataUpdateCoordinator


type ObegransadConfigEntry = ConfigEntry[ObegransadRuntimeData]
