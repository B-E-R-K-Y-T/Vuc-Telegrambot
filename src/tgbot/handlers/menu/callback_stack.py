from copy import copy
from functools import wraps
from typing import Callable, Awaitable, Optional, Any, Coroutine

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from exceptions import FunctionStackEmpty, StackRoot
from tgbot.services.utils.message_tools import get_message
from tgbot.services.utils.util import sync_async_call


class CallFunctionStack:
    def __init__(self):
        self.__stack = {}

    def get_last_call(self, chat_id: int):
        if chat_id not in self.__stack:
            return None

        if len(self.__stack[chat_id]) == 1:
            return None

        function_image = copy(self.__stack[chat_id][-2])
        self.__stack[chat_id].pop(-1)

        return function_image

    def add(
            self,
            func: Callable | Awaitable,
            metadata: Message | CallbackQuery,
            bot: AsyncTeleBot,
            args,
            kwargs
    ):
        message: Message = get_message(metadata)
        chat_id: int = message.chat.id

        if chat_id not in self.__stack:
            self.__stack[chat_id]: dict = []

        if not args and not kwargs:
            self.__stack[chat_id].append((func, metadata, bot))
        elif not args:
            self.__stack[chat_id].append((func, metadata, bot, kwargs))
        elif not kwargs:
            self.__stack[chat_id].append((func, metadata, bot, args))
        else:
            self.__stack[chat_id].append((func, metadata, bot, args, kwargs))

    def clear(self):
        self.__stack.clear()

    def get_stack(self):
        return self.__stack.copy()


class CallbackCollector:
    def __init__(self, stack: CallFunctionStack):
        self.__stack = stack

    def root(self, func: Callable | Awaitable) -> Callable[
        [Message | CallbackQuery, AsyncTeleBot, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs):
            self.__stack.clear()
            self.__stack.add(func, metadata, bot, args, kwargs)

            return await sync_async_call(func, metadata, bot, *args, **kwargs)

        return wrapper

    def listen_call(self, func: Callable | Awaitable) -> Callable[
        [Message | CallbackQuery, AsyncTeleBot, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs):
            self.__stack.add(func, metadata, bot, args, kwargs)

            return await sync_async_call(func, metadata, bot, *args, **kwargs)

        return wrapper


class StackStrider:
    def __init__(self, stack: CallFunctionStack, collector: CallbackCollector):
        self.__stack = stack
        self.__collector = collector

    async def back(self, chat_id: int):
        print(self.__stack.get_stack())
        function_image: Optional[tuple] = self.__stack.get_last_call(chat_id)

        if function_image is not None:
            func = function_image[0]
            self.__collector.listen_call(func)

        if function_image is None:
            raise FunctionStackEmpty

        await sync_async_call(*function_image)

        if len(self.__stack.get_stack()[chat_id]) == 1:
            raise StackRoot
