from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.api_worker.client import APIWorker
from tgbot.user import User
from tgbot.utils.database import Database
from tgbot.utils.message_tools import send_wait_smile


@send_wait_smile
async def logout_handler(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await User(message.from_user.id).ainit()
    db = Database()

    if await api.logout(user.token):
        await db.del_value(str(message.from_user.id))
        await bot.send_message(message.chat.id, "Вы вышли из аккаунта.")
    else:
        await bot.send_message(message.chat.id, "Ошибка.")
