import asyncio
from copy import copy
from functools import wraps
from pprint import pprint
from typing import Callable

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, Update
from typing_extensions import Awaitable

from tgbot.utils.message_tools import get_message


class _auto_callback_data:
    state = 0

    def __new__(cls, *args, **kwargs):
        cls.state += 1

        return str(cls.state)


class CallBackStackWorker:
    def __init__(self):
        self.__stack: dict[int, list[dict[Callable | Awaitable, tuple]]] = {}
        self.__root: dict = {}

    def get_root_id(self, chat_id: int) -> int | None:
        return self.__root.get(chat_id)

    def set_root_id(self, chat_id: int, metadata: Message | CallbackQuery) -> None:
        self.__root[chat_id] = get_message(metadata).message_id

    async def __call(
            self,
            chat_id: int,
            func: Callable | Awaitable,
            bot: AsyncTeleBot,
            metadata: Message | CallbackQuery,
            is_root: bool,
            *args,
            **kwargs
    ) -> None:
        self.add_call(
            chat_id,
            func,
            bot,
            metadata,
            get_message(metadata).message_id,
            is_root=is_root,
        )

        if asyncio.iscoroutinefunction(func):
            await func(metadata, bot, )
        else:
            func(metadata, bot, *args, **kwargs)

    def __replace_metadata_in_chat(self, chat_id: int, metadata: Message | CallbackQuery) -> None:
        new_metadata = {}

        for idx, call_obj in enumerate(self.__stack[chat_id]):
            for func, (old_metadata, bot, message_id, is_root) in call_obj.items():
                new_metadata[func] = (metadata, bot, message_id, is_root)

            for func in new_metadata.keys():
                call_obj[func] = new_metadata[func]

    def resend(self, func: Callable | Awaitable) -> Callable | Awaitable:
        raise Warning('Нуждается в доработке')

        # async def wrapper(metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs):
        #     chat_id = get_message(metadata).chat.id
        #     if not self.__stack[chat_id]:
        #         return
        #
        #     if asyncio.iscoroutinefunction(func):
        #         await func(metadata, bot, *args, **kwargs)
        #     else:
        #         func(metadata, bot, *args, **kwargs)
        #
        #     func_, (metadata_, bot_, _, is_root) = self.__stack[chat_id][-1].popitem()
        #     del self.__stack[chat_id][-1]
        #
        #     message = get_message(metadata_)
        #     await bot.delete_message(message.chat.id, message.message_id)
        #
        #     new_metadata = await bot.send_message(message.chat.id, message.text)
        #
        #     self.__replace_metadata_in_chat(message.chat.id, new_metadata)
        #
        #     res = await self.__call(
        #         chat_id=chat_id,
        #         func=func_,
        #         metadata=new_metadata,
        #         bot=bot_,
        #         is_root=is_root,
        #     )
        #
        #     return res
        #
        # return wrapper

    def add_call(
            self,
            chat_id: int,
            func: Callable,
            bot: AsyncTeleBot,
            metadata: Message | CallbackQuery,
            message_id,
            is_root: bool = False,
    ):
        if self.__stack.get(chat_id) is None:
            self.__stack[chat_id] = []

        self.__stack[chat_id].append({func: (metadata, bot, message_id, is_root)})

    def go_root(self, func: Callable | Awaitable) -> Callable | Awaitable:
        @wraps(func)
        async def wrapper(
                metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs
        ):
            chat_id = get_message(metadata).chat.id
            if not self.__stack[chat_id]:
                return

            root_func, (root_metadata, root_bot, _, is_root) = self.__stack[chat_id][0].popitem()

            if is_root:
                await bot.delete_message(
                    chat_id=chat_id, message_id=self.get_root_id(chat_id)
                )

            self.__stack.clear()

            if asyncio.iscoroutinefunction(func):
                await func(metadata, bot, *args, **kwargs)
            else:
                func(metadata, bot, *args, **kwargs)

            return await self.__call(
                chat_id=chat_id,
                func=root_func,
                metadata=root_metadata,
                bot=bot,
                is_root=is_root,
            )

        return wrapper

    def get_last_call(self, chat_id: int) -> dict:
        if self.__stack.get(chat_id) is not None:
            if len(self.__stack[chat_id]) >= 2:
                call = copy(self.__stack[chat_id][-2])
                self.__stack[chat_id].pop(-1)
                return call

    def listen_call(self, is_root: bool = False):
        def decorator(func):
            @wraps(func)
            async def wrapper(
                    metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs
            ) -> Callable:
                message = get_message(metadata)

                chat_id = message.chat.id
                message_id = message.message_id

                if is_root:
                    if chat_id in self.__stack:
                        self.__stack[chat_id].clear()

                self.add_call(chat_id, func, bot, metadata, message_id, is_root=is_root)

                if asyncio.iscoroutinefunction(func):
                    return await func(metadata, bot, *args, **kwargs)
                else:
                    return func(metadata, bot, *args, **kwargs)

            return wrapper

        return decorator

    def __repr__(self):
        return f"<{self.__class__.__name__}> STACK: {self.__stack}"


class CallBackData:
    MARK = _auto_callback_data()
    ATTEND = _auto_callback_data()
    EDIT_PERSONAL_DATA = _auto_callback_data()
    PERSONAL_DATA = _auto_callback_data()

    SEMESTER_ONE = _auto_callback_data()
    SEMESTER_TWO = _auto_callback_data()
    SEMESTER_THREE = _auto_callback_data()
    SEMESTER_FOUR = _auto_callback_data()
    SEMESTER_FIVE = _auto_callback_data()
    SEMESTER_SIX = _auto_callback_data()

    STUDENT_MENU = _auto_callback_data()
    SQUAD_MENU = _auto_callback_data()
    PLATOON_MENU = _auto_callback_data()

    ADD_STUDENT = _auto_callback_data()
    MOVE_STUDENT = _auto_callback_data()

    NAME = _auto_callback_data()
    DOB = _auto_callback_data()
    PHONE = _auto_callback_data()
    EMAIL = _auto_callback_data()
    ADDRESS = _auto_callback_data()
    INSTITUTE = _auto_callback_data()
    DOS = _auto_callback_data()
    GROUP_STUDY = _auto_callback_data()
    PLATOON_NUMBER = _auto_callback_data()
    SQUAD_NUMBER = _auto_callback_data()
    ROLE = _auto_callback_data()
    TELEGRAM_ID = _auto_callback_data()

    BACK = _auto_callback_data()
    REOPEN_MENU = _auto_callback_data()


__all__ = (
    CallBackData.__name__,
    CallBackStackWorker.__name__,
)
