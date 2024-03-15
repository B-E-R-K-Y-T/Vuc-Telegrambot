from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from exceptions import ErrorMessage
from tgbot.handlers.menu import menu_handler
from tgbot.states.login import Login
from tgbot.api_worker.client import APIWorker
from tgbot.user import User
from tgbot.utils.database import Database
from tgbot.utils.message_tools import send_wait_smile
from tgbot.validators.validate import check_valid_email
from tgbot.validators.validator_handler import bind_validator

_users = {}
_db = Database()
_api = APIWorker()


async def login_handler_init(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    user = await User(usr_id).ainit()

    jwt = user.token

    if jwt is not None:
        await bot.send_message(message.chat.id, "Вы уже вошли в систему.")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        _users[usr_id] = user

        await bot.send_message(message.chat.id, "Введите свою почту:")
        await bot.set_state(message.from_user.id, Login.email, message.chat.id)


@bind_validator(validator=check_valid_email, msg_err=ErrorMessage.EMAIL_INVALID_FORMAT)
async def login_handler_email(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    _users[usr_id].set_email(message.text)

    await bot.send_message(message.chat.id, "Ок, введите свой пароль:")
    await bot.set_state(message.from_user.id, Login.password, message.chat.id)


@send_wait_smile
async def login_handler_password(message: Message, bot: AsyncTeleBot):
    usr_id = message.from_user.id
    user = _users[usr_id]
    user.password = message.text

    # Удаляем пароль пользователя из чата
    await bot.delete_message(message.chat.id, message.message_id)

    jwt = await _api.login(await user.get_email(), user.password)

    if jwt is None:
        await bot.send_message(message.chat.id, "Ошибка.")
    else:
        await _db.set_value(
            key=str(usr_id), value=[message.date, jwt, await user.get_email()]
        )

        await bot.send_message(message.chat.id, "Успешно.")

        await menu_handler(message, bot)

    await bot.delete_state(message.from_user.id, message.chat.id)
    del _users[usr_id]
