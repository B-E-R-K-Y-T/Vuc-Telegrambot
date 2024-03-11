from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.api_worker.client import APIWorker
from tgbot.user import User
from tgbot.utils.database import Database


async def logout_handler(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = User(message.from_user.id)
    db = Database()

    if await api.logout(await user.get_jwt()):
        await db.del_value(str(message.from_user.id))
        await bot.send_message(message.chat.id, 'Вы вышли из аккаунта.')
    else:
        await bot.send_message(message.chat.id, 'Ошибка.')
