import aiohttp

from config import app_settings


class Request:
    def __init__(self):
        self.base_url = f'http://{app_settings.SERVER_HOST}:{app_settings.SERVER_PORT}'

    async def __request(self, endpoint: str, *, data: dict = None, headers: dict = None, method: str = ''):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with getattr(session, method)(f'{self.base_url}{endpoint}', data=data) as resp:
                return resp

    async def get(self, endpoint: str, *, data: dict = None, headers: dict = None):
        return await self.__request(endpoint, data=data, headers=headers, method='get')

    async def post(self, endpoint: str, *, data: dict = None, headers: dict = None):
        return await self.__request(endpoint, data=data, headers=headers, method='post')

    async def patch(self, endpoint: str, *, data: dict = None, headers: dict = None):
        return await self.__request(endpoint, data=data, headers=headers, method='patch')
