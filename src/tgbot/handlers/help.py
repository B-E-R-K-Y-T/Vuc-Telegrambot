from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from config import Roles
from tgbot.services.commands import CommandSequence
from tgbot.services.outline_text_buttons import OutlineKeyboardButton
from tgbot.services.user import UsersFactory, User
from tgbot.services.utils.message_tools import send_status_task_smile
from exceptions import BackgroundTaskError


@send_status_task_smile()
async def cmd_help(message: Message, bot: AsyncTeleBot):
    user: User = await UsersFactory().get_user(message)
    chat_id: int = message.chat.id

    if await user.token is None:
        await bot.send_message(
            chat_id,
            f"Чтобы пользоваться ботом. Введите команду /{CommandSequence.LOGIN} "
            f"или нажмите на кнопку \"{OutlineKeyboardButton.LOGIN}\" либо пройдите регистрацию:"
            f"/{CommandSequence.REG} ",
        )
    elif await user.role == Roles.student:
        await bot.send_message(
            chat_id,
            f"Откройте меню, чтобы пользоваться ботом: /{CommandSequence.LOGIN} ",
        )
    elif await user.role == Roles.squad_commander:
        await bot.send_message(
            chat_id,
            f"Откройте меню, чтобы пользоваться ботом: /{CommandSequence.LOGIN} "
        )
    elif await user.role == Roles.platoon_commander:
        await bot.send_message(
            chat_id,
            f"Откройте меню, чтобы пользоваться ботом: /{CommandSequence.LOGIN} "
        )
    elif await user.role == Roles.professor:
        await bot.send_message(
            chat_id,
            f"Откройте меню, чтобы пользоваться ботом: /{CommandSequence.LOGIN} "
        )
    elif await user.role == Roles.admin:
        await bot.send_message(
            chat_id,
            f"Откройте меню, чтобы пользоваться ботом: /{CommandSequence.LOGIN} "
        )
    else:
        raise BackgroundTaskError
