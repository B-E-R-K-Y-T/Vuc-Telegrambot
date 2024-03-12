from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.api_worker.client import APIWorker
from tgbot.user import User


async def menu_handler(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = User(message.from_user.id)
    token = await user.get_jwt()
    user_id: int = await api.get_id_from_tg(token, user.tg_id)
    print(user_id)
    role = await api.get_user_role(token, user_id)

    print(token, user_id, role)

    await bot.send_message(message.chat.id, f'MENU, {role=}')
