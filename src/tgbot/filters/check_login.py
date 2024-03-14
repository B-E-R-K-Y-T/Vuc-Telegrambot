from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

from tgbot.user import User


class CheckLogin(SimpleCustomFilter):
    key = "check_login"

    def __init__(self, bot):
        self.bot: AsyncTeleBot = bot

    async def check(self, message: Message):
        user = await User(message.from_user.id).ainit()

        if await user.get_jwt() is None:
            await self.bot.send_message(message.chat.id, "Вы не вошли в систему.")
            return False

        return True
