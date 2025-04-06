from datetime import timedelta
from typing import Final

from homeassistant.const import Platform

NAME: Final = "Obegränsad"

DOMAIN: Final = "obegransad"

ATTR_CONFIG_ENTRY_ID: Final = "config_entry_id"

ATTR_TEXT: Final = "text"
ATTR_GRAPH: Final = "graph"
ATTR_MIN_Y: Final = "min_y"
ATTR_MAX_Y: Final = "max_y"
ATTR_REPEAT: Final = "repeat"
ATTR_MESSAGE_ID: Final = "message_id"
ATTR_DELAY: Final = "delay"
ATTR_SCHEDULE: Final = "schedule"
ATTR_PLUGIN_ID: Final = "plugin_id"
ATTR_DURATION: Final = "duration"

DATA_HASS_CONFIG: Final = "hass_config"

SERVICE_SET_SCHEDULE: Final = "set_schedule"
SERVICE_REMOVE_MESSAGE: Final = "remove_message"
SERVICE_CLEAR_STORAGE: Final = "clear_storage"

UPDATE_INTERVAL: Final = timedelta(seconds=10)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.LIGHT,
    Platform.SWITCH,
]
