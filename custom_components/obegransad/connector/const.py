from typing import Final

from aiohttp import ClientTimeout

API_BASE_URL: Final = "http://{host}/api"
API_URL_INFO: Final = API_BASE_URL + "/info"
API_URL_PLUGIN: Final = API_BASE_URL + "/plugin"
API_URL_BRIGHTNESS: Final = API_BASE_URL + "/brightness"
API_URL_DATA: Final = API_BASE_URL + "/data"
API_URL_SCHEDULE: Final = API_BASE_URL + "/schedule"
API_URL_SCHEDULE_START: Final = API_URL_SCHEDULE + "/start"
API_URL_SCHEDULE_STOP: Final = API_URL_SCHEDULE + "/stop"
API_URL_MESSAGE: Final = API_BASE_URL + "/message"
API_URL_REMOVE_MESSAGE: Final = API_BASE_URL + "/removemessage"
API_URL_CLEAR_STORAGE: Final = API_BASE_URL + "/clearstorage"

TIMEOUT = ClientTimeout(total=10)
