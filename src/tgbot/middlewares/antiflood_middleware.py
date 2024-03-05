from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.async_telebot import CancelUpdate


class UserMessageCounter:
    def __init__(self, message):
        self.__message = message
        self.__count: int = 1

    @property
    def message(self):
        return self.__message

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value: int):
        self.__count = value


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, timeout, max_messages, bot) -> None:
        super().__init__()

        self.messages: dict[UserMessageCounter] = {}
        self.timeout = timeout
        self.max_messages = max_messages
        self.update_types = ["message"]
        self.bot = bot

    async def pre_process(self, message, data):
        msg_id = message.from_user.id

        if msg_id not in self.messages:
            self.messages[msg_id] = UserMessageCounter(message)
            return

        user_message = self.messages[msg_id]
        user_message_count = user_message.count
        user_message_date = user_message.message.date

        if user_message_count >= self.max_messages:
            if message.date - user_message_date < self.timeout:
                await self.bot.send_message(
                    message.chat.id,
                    f"Вы отправляете сообщения слишком часто. "
                    f"Через {self.timeout} секунд(ы) вы сможете снова отправлять их.",
                )
                return CancelUpdate()
            else:
                self.messages[message.from_user.id] = UserMessageCounter(message)
                self.messages[message.from_user.id].count = 1
        else:
            user_message.count += 1

        user_message.message.date = message.date

    async def post_process(self, message, data, exception):
        pass
