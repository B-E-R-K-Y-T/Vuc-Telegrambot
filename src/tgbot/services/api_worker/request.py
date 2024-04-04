from http import HTTPStatus
from json import JSONEncoder
from typing import Optional

import aiohttp

from config import app_settings
from exceptions import TooManyRequestsError
from logger import LOGGER


class Request:
    def __init__(
            self,
            base_url: str = f"http://{app_settings.SERVER_HOST}:{app_settings.SERVER_PORT}",
    ):
        self.base_url = base_url

    async def __request(
            self,
            endpoint: str,
            *,
            data: Optional[dict | JSONEncoder] = None,
            headers: Optional[dict] = None,
            method: str = "",
            cookies: Optional[dict] = None,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
            **kwargs,
    ):
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with getattr(session, method)(
                        f"{self.base_url}{endpoint}",
                        data=data,
                        cookies=cookies,
                        params=params,
                        json=json,
                        **kwargs,
                ) as resp:
                    if resp.status == HTTPStatus.TOO_MANY_REQUESTS:
                        raise TooManyRequestsError

                    yield resp
            except aiohttp.ClientError as e:
                LOGGER.error(str(e))

                yield None

    async def get(
            self,
            endpoint: str,
            *,
            data: Optional[dict] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            params: Optional[dict] = None,
            **kwargs,
    ):
        return await anext(
            self.__request(
                endpoint,
                data=data,
                headers=headers,
                method="get",
                cookies=cookies,
                params=params,
                **kwargs,
            )
        )

    async def post(
            self,
            endpoint: str,
            *,
            data: Optional[dict] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
            **kwargs,
    ):
        return await anext(
            self.__request(
                endpoint,
                data=data,
                headers=headers,
                method="post",
                cookies=cookies,
                params=params,
                json=json,
                **kwargs,
            )
        )

    async def patch(
            self,
            endpoint: str,
            *,
            data: Optional[dict | JSONEncoder] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            params: Optional[dict] = None,
            json: Optional[dict] = None,
            **kwargs,
    ):
        return await anext(
            self.__request(
                endpoint,
                data=data,
                headers=headers,
                method="patch",
                cookies=cookies,
                params=params,
                json=json,
                **kwargs,
            )
        )
