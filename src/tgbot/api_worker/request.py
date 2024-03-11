import aiohttp

from config import app_settings


class Request:
    def __init__(self):
        self.base_url = f"http://{app_settings.SERVER_HOST}:{app_settings.SERVER_PORT}"

    async def __request(
        self,
        endpoint: str,
        *,
        data: dict = None,
        headers: dict = None,
        method: str = "",
        cookies: dict = None,
        **kwargs,
    ):
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with getattr(session, method)(
                    f"{self.base_url}{endpoint}", data=data, cookies=cookies, **kwargs
                ) as resp:
                    return resp
            except aiohttp.ClientError:
                return None

    async def get(
        self,
        endpoint: str,
        *,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        **kwargs,
    ):
        return await self.__request(
            endpoint,
            data=data,
            headers=headers,
            method="get",
            cookies=cookies,
            **kwargs,
        )

    async def post(
        self,
        endpoint: str,
        *,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        **kwargs,
    ):
        return await self.__request(
            endpoint,
            data=data,
            headers=headers,
            method="post",
            cookies=cookies,
            **kwargs,
        )

    async def patch(
        self,
        endpoint: str,
        *,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        **kwargs,
    ):
        return await self.__request(
            endpoint,
            data=data,
            headers=headers,
            method="patch",
            cookies=cookies,
            **kwargs,
        )
