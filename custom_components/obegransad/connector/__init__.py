import json
import logging
from typing import Any, Self

from aiohttp import ClientSession

from .const import (
    API_URL_INFO,
    API_URL_BRIGHTNESS,
    API_URL_PLUGIN,
    TIMEOUT,
    API_URL_MESSAGE,
    API_URL_SCHEDULE,
    API_URL_SCHEDULE_START,
    API_URL_SCHEDULE_STOP,
    API_URL_REMOVE_MESSAGE,
    API_URL_CLEAR_STORAGE,
)
from .exceptions import (
    ObegransadApiException,
)
from .model import ObegransadDeviceData

_LOGGER = logging.getLogger(__name__)


class ObegransadConnector:
    _session: ClientSession
    _host: str
    _last_brightness: int | None

    def __init__(self: Self, session: ClientSession, host: str) -> None:
        self._session = session
        self._host = host
        self._last_brightness = None

    async def _get_data(self: Self, url: str) -> Any:
        response = await self._session.get(url, timeout=TIMEOUT)

        response_text = await response.text()

        if response.status != 200:
            raise ObegransadApiException(response.status, response_text)

        return json.loads(response_text)

    async def get_data(self: Self) -> ObegransadDeviceData:
        url = API_URL_INFO.format(host=self._host)
        data = await self._get_data(url)
        obegransad_device_data = ObegransadDeviceData.from_dict(data)
        if obegransad_device_data.brightness != 0:
            self._last_brightness = obegransad_device_data.brightness
        return obegransad_device_data

    async def set_brightness(self: Self, brightness: int | None) -> None:
        if brightness is None:
            brightness_value = self._last_brightness or 255
        else:
            brightness_value = brightness
        url = API_URL_BRIGHTNESS.format(host=self._host)
        await self._session.patch(
            url, data={"value": brightness_value}, timeout=TIMEOUT
        )

    async def set_plugin(self: Self, plugin_id: int) -> None:
        url = API_URL_PLUGIN.format(host=self._host)
        await self._session.patch(url, data={"id": plugin_id}, timeout=TIMEOUT)

    async def display_message(
        self: Self,
        text: str | None,
        graph: list[int] | None,
        min_y: int | None,
        max_y: None,
        repeat: int | None,
        message_id: str | None,
        delay: int | None,
    ) -> None:
        url = API_URL_MESSAGE.format(host=self._host)
        data = {}
        if text is not None and text != "":
            data["text"] = text
        if graph is not None:
            data["graph"] = ",".join(list(map(lambda g: str(g), graph)))
        if min_y is not None:
            data["miny"] = min_y
        if max_y is not None:
            data["maxy"] = max_y
        if repeat is not None:
            data["repeat"] = repeat
        if message_id is not None:
            data["id"] = message_id
        if delay is not None:
            data["delay"] = delay
        await self._session.get(url, data=data, timeout=TIMEOUT)

    async def remove_message(self: Self, message_id: str) -> None:
        url = API_URL_REMOVE_MESSAGE.format(host=self._host)
        data = {"id": message_id}
        await self._session.get(url, data=data, timeout=TIMEOUT)

    async def start_schedule(self: Self) -> None:
        url = API_URL_SCHEDULE_START.format(host=self._host)
        await self._session.get(url, timeout=TIMEOUT)

    async def stop_schedule(self: Self) -> None:
        url = API_URL_SCHEDULE_STOP.format(host=self._host)
        await self._session.get(url, timeout=TIMEOUT)

    async def set_schedule(self: Self, schedule_data: list[dict[str, int]]) -> None:
        url = API_URL_SCHEDULE.format(host=self._host)
        response = await self._session.post(
            url,
            data={
                "schedule": json.dumps(schedule_data).replace("plugin_id", "pluginId")
            },
            timeout=TIMEOUT,
        )
        text = await response.text()
        print(text)

    async def clear_storage(self: Self) -> None:
        url = API_URL_CLEAR_STORAGE.format(host=self._host)
        await self._session.get(url, timeout=TIMEOUT)
