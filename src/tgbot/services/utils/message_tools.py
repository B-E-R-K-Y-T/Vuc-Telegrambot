import asyncio
from functools import wraps
from typing import Callable, Any

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from typing_extensions import Awaitable

from logger import LOGGER


def get_message(metadata: Message | CallbackQuery) -> Message:
    if isinstance(metadata, Message):
        return metadata
    elif isinstance(metadata, CallbackQuery):
        return metadata.message
    else:
        raise TypeError


async def send_temp_smile(message: Message, bot: AsyncTeleBot, smile: str, lifetime_smile: float = 2.5):
    msg = await bot.send_message(message.chat.id, smile)
    await asyncio.sleep(lifetime_smile)
    await bot.delete_message(message.chat.id, msg.message_id)


def send_status_task_smile(
        *,
        send_success_status_smile: bool = True,
        lifetime_smile: float = 2.5,
        success_smile: str = "✅",
        failed_smile: str = "❌",
        waiting_smile: str = "⏳",
):
    if not send_success_status_smile:
        lifetime_smile = 0

    def decorator(func: Callable | Awaitable) -> Callable | Awaitable:
        @wraps(func)
        async def wrapper(
                metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args: Any, **kwargs: Any
        ) -> Any:
            message: Message = get_message(metadata)
            msg_process: Message = await bot.send_message(message.chat.id, waiting_smile)

            try:
                if asyncio.iscoroutinefunction(func):
                    res = await func(metadata, bot, *args, **kwargs)
                else:
                    res = func(metadata, bot, *args, **kwargs)
            except Exception as e:
                LOGGER.error(str(e))

                await bot.edit_message_text(failed_smile, message.chat.id, msg_process.message_id)
            else:
                if send_success_status_smile:
                    await bot.edit_message_text(success_smile, message.chat.id, msg_process.message_id)
                return res
            finally:
                await asyncio.sleep(lifetime_smile)
                await bot.delete_message(message.chat.id, msg_process.message_id)

        return wrapper

    return decorator
