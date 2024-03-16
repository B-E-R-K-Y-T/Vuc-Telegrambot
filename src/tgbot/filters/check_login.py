from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

from tgbot.services.user import UsersFactory
from tgbot.services.commands import CommandSequence


class CheckLogin(SimpleCustomFilter):
    key = "check_login"

    def __init__(self, bot):
        self.bot: AsyncTeleBot = bot

    async def check(self, message: Message):
        user = await UsersFactory().get_user(message)

        if await user.token is None:
            await self.bot.send_message(
                message.chat.id,
                f"Вы не вошли в систему.\n\n"
                f"Чтобы войти, используйте команду: /{CommandSequence.LOGIN}",
            )
            return False

        return True
