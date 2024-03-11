from collections import deque

from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.async_telebot import CancelUpdate, AsyncTeleBot
from telebot.types import Message


class UserMessage:
    def __init__(self, max_messages: int):
        self.message_deque = deque(maxlen=max_messages)
        self.is_ban = False


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, timeout: int, interval: int, max_messages, bot: AsyncTeleBot):
        super().__init__()

        self.messages: dict[int, UserMessage] = {}
        self.timeout = timeout
        self.interval = interval
        self.max_messages = max_messages
        self.update_types = ["message"]
        self.bot: AsyncTeleBot = bot

    async def __send_ban_message(self, message: Message, timeout: int):
        await self.bot.send_message(message.chat.id, f'Вы отправляете запросы слишком часто. '
                                                     f'Подождите {timeout} секунд.')
        return CancelUpdate()

    async def pre_process(self, message: Message, data):
        user_id = message.from_user.id

        if user_id not in self.messages:
            self.messages[user_id] = UserMessage(self.max_messages)

        user_message = self.messages[user_id]

        if user_message.is_ban:
            if message.date - user_message.message_deque[-1].date < self.timeout:
                return await self.__send_ban_message(
                    message=message,
                    timeout=self.timeout - (message.date - user_message.message_deque[-1].date)
                )
            else:
                user_message.is_ban = False

        if user_message.message_deque:
            if message.date - user_message.message_deque[0].date > self.interval:
                user_message.message_deque.clear()

        if len(user_message.message_deque) < self.max_messages:
            user_message.message_deque.append(message)
        elif message.date - user_message.message_deque[0].date < self.interval:
            user_message.is_ban = True
            return await self.__send_ban_message(message, self.timeout)

    async def post_process(self, message: Message, data, exception):
        pass
