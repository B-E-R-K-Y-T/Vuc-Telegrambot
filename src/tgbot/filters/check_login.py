from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message

from tgbot.user import User


class CheckLogin(SimpleCustomFilter):

    key = 'check_login'

    def __init__(self, bot):
        self.bot = bot

    async def check(self, message: Message):
        user = User(message.from_user.id)

        if await user.get_jwt() is None:
            await self.bot.send_message(message.chat.id, 'Вы не вошли в систему.')
            return False
        else:
            return True
