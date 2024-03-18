import asyncio
from functools import wraps
from typing import Callable

from typing_extensions import Awaitable


def bind_validator(
        validator: Callable | Awaitable,
        msg_err: str = "Ошибка. Текст не прошел валидацию, попробуйте ещё раз."
) -> Callable:
    def decorator(func: Callable | Awaitable) -> Callable | Awaitable:
        @wraps(func)
        async def wrapper(message, bot, *args, **kwargs):
            if await validator(message=message):
                if asyncio.iscoroutinefunction(func):
                    return await func(bot=bot, message=message, *args, **kwargs)
                else:
                    return func(bot=bot, message=message, *args, **kwargs)
            else:
                await bot.send_message(message.chat.id, msg_err)

        return wrapper

    return decorator
