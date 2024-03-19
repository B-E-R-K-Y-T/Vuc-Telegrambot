from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from config import Roles
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
            f"Help для не залогиненого чела",
        )
    elif await user.role == Roles.student:
        await bot.send_message(
            chat_id,
            f"Help для Roles.student",
        )
    elif await user.role == Roles.squad_commander:
        await bot.send_message(
            chat_id,
            f"Help для Roles.squad_commander",
        )
    elif await user.role == Roles.platoon_commander:
        await bot.send_message(
            chat_id,
            f"Help для Roles.platoon_commander",
        )
    elif await user.role == Roles.professor:
        await bot.send_message(
            chat_id,
            f"Help для Roles.professor",
        )
    elif await user.role == Roles.admin:
        await bot.send_message(
            chat_id,
            f"Help для Roles.admin",
        )
    else:
        raise BackgroundTaskError
