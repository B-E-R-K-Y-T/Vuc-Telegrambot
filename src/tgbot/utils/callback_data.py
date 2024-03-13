import asyncio
from functools import wraps
from typing import Callable

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery


class _auto_callback_data:
    state = 0

    def __new__(cls, *args, **kwargs):
        object.__new__(cls)

        cls.state += 1

        return str(cls.state)


class CallBackStackWorker:
    def __init__(self):
        self.__stack: dict[int, list[dict[Callable, tuple]]] = {}

    def add_call(
        self,
        chat_id: int,
        func: Callable,
        bot: AsyncTeleBot,
        metadata: Message | CallbackQuery,
    ):
        if self.__stack.get(chat_id) is None:
            self.__stack[chat_id] = []

        self.__stack[chat_id].append({func: (metadata, bot)})

    def get_last_call(self, chat_id: int) -> dict:
        if self.__stack.get(chat_id) is not None:
            if len(self.__stack[chat_id]) >= 2:
                return self.__stack[chat_id].pop(-2)

    def listen_call(self, func):
        @wraps(func)
        async def wrapper(
            metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs
        ) -> Callable:
            if isinstance(metadata, Message):
                chat_id = metadata.chat.id
            elif isinstance(metadata, CallbackQuery):
                chat_id = metadata.message.chat.id
            else:
                raise TypeError

            self.add_call(
                chat_id,
                func,
                bot,
                metadata
            )

            if asyncio.iscoroutinefunction(func):
                return await func(metadata, bot, *args, **kwargs)
            else:
                return func(metadata, bot, *args, **kwargs)

        return wrapper

    def get_len_stack_chat(self, chat_id: int) -> int:
        if chat_id in self.__stack:
            return len(self.__stack[chat_id])

    def __repr__(self):
        return f"<{self.__class__.__name__}> STACK: {self.__stack}"


class CallBackData:
    MARK = _auto_callback_data()
    ATTEND = _auto_callback_data()
    SELF_DATA = _auto_callback_data()

    SEMESTER_ONE = _auto_callback_data()
    SEMESTER_TWO = _auto_callback_data()
    SEMESTER_THREE = _auto_callback_data()
    SEMESTER_FOUR = _auto_callback_data()
    SEMESTER_FIVE = _auto_callback_data()
    SEMESTER_SIX = _auto_callback_data()

    STUDENT_MENU = _auto_callback_data()
    SQUAD_MENU = _auto_callback_data()
    PLATOON_MENU = _auto_callback_data()

    BACK = _auto_callback_data()


__all__ = (
    CallBackData.__name__,
)
