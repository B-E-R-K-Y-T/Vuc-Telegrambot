from redis import asyncio as aioredis

from config import app_settings


class Database:
    def __init__(self) -> None:
        self.redis = aioredis.from_url(f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}")

    async def set_value(self, key: str, value):
        await self.redis.set(key, value)

    async def get_value(self, key: str):
        return await self.redis.get(key)

    async def del_value(self, key: str):
        await self.redis.delete(key)
