import asyncio
from typing import Callable, Awaitable, Any


async def sync_async_call(func: Callable | Awaitable, *args: Any, **kwargs: Any) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)
