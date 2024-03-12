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
            params: dict = None,
            **kwargs,
    ):
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with getattr(session, method)(
                        f"{self.base_url}{endpoint}", data=data, cookies=cookies, params=params, **kwargs
                ) as resp:
                    yield resp
            except aiohttp.ClientError:
                yield None

    async def get(
            self,
            endpoint: str,
            *,
            data: dict = None,
            headers: dict = None,
            cookies: dict = None,
            params: dict = None,
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
            data: dict = None,
            headers: dict = None,
            cookies: dict = None,
            params: dict = None,
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
                **kwargs,
            )
        )

    async def patch(
            self,
            endpoint: str,
            *,
            data: dict = None,
            headers: dict = None,
            cookies: dict = None,
            params: dict = None,
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
                **kwargs,
            )
        )
