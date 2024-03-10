from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.states.login import Login
from tgbot.api_worker.client import APIWorker
from tgbot.user import User
from tgbot.utils.database import Database

users = {}
db = Database()
api = APIWorker()


async def login_handler_init(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    user = User(usr_id)

    jwt = await user.get_jwt()

    if jwt is not None:
        await bot.send_message(message.chat.id, "Вы уже вошли в систему.")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        users[usr_id] = user

        await bot.send_message(message.chat.id, "Введите свою почту: ")
        await bot.set_state(message.from_user.id, Login.name, message.chat.id)


async def login_handler_name(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    users[usr_id].username = message.text

    await bot.send_message(message.chat.id, "Ок, введите свой пароль:")
    await bot.set_state(message.from_user.id, Login.password, message.chat.id)


async def login_handler_password(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    user = users[usr_id]
    user.password = message.text

    await bot.send_message(message.chat.id, "Обрабатываю запрос...")

    jwt = await api.login(user.username, user.password)

    if jwt is None:
        await bot.send_message(message.chat.id, 'Неверные данные.')
    else:
        await bot.send_message(message.chat.id, 'Успешно.')

        await db.set_value(key=str(usr_id), value=jwt)

    await bot.delete_state(message.from_user.id, message.chat.id)
    del users[usr_id]
