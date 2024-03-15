import asyncio
from functools import wraps
from typing import Callable

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery


def get_message(metadata: Message | CallbackQuery) -> Message:
    if isinstance(metadata, Message):
        return metadata
    elif isinstance(metadata, CallbackQuery):
        return metadata.message
    else:
        raise TypeError


def send_wait_smile(func: Callable):
    @wraps(func)
    async def wrapper(
        metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs
    ):
        message = get_message(metadata)

        msg_id: Message = await bot.send_message(message.chat.id, "⏳")

        if asyncio.iscoroutinefunction(func):
            res = await func(metadata, bot, *args, **kwargs)
        else:
            res = func(metadata, bot, *args, **kwargs)

        await bot.delete_message(message.chat.id, msg_id.message_id)

        return res

    return wrapper