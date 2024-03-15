from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

from tgbot.user import User
from tgbot.commands import CommandSequence


class CheckLogin(SimpleCustomFilter):
    key = "check_login"

    def __init__(self, bot):
        self.bot: AsyncTeleBot = bot

    async def check(self, message: Message):
        user = await User(message.from_user.id).ainit()

        if user.token is None:
            await self.bot.send_message(
                message.chat.id,
                f"Вы не вошли в систему.\n\n"
                f"Чтобы войти, используйте команду: /{CommandSequence.LOGIN}",
            )
            return False

        return True
