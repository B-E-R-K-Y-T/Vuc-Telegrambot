# aioredis
from redis import asyncio as aioredis


# Create a connection
class Database:
    def __init__(self) -> None:
        self.redis = aioredis.from_url("redis://localhost")
