from datetime import date

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from config import Roles
from exceptions import ErrorMessage
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.user import UsersFactory, User
from tgbot.services.utils.message_tools import send_status_task_smile, send_temp_smile
from tgbot.services.validators.validate import check_valid_date
from tgbot.services.validators.validator_handler import bind_validator

_api = APIWorker()


@bind_validator(validator=check_valid_date, msg_err=ErrorMessage.DATE_INVALID_FORMAT)
async def set_positive_attend(message: Message, bot: AsyncTeleBot):
    current_user: User = await UsersFactory().get_user(message)

    await set_attend(message, bot, current_user, visiting=1)
    await bot.delete_state(message.chat.id, message.chat.id)
    # await bot.send_message(message.chat.id, "Успешно!")


@bind_validator(validator=check_valid_date, msg_err=ErrorMessage.DATE_INVALID_FORMAT)
async def set_negative_attend(message: Message, bot: AsyncTeleBot):
    current_user: User = await UsersFactory().get_user(message)

    await set_attend(message, bot, current_user, visiting=0)
    await bot.delete_state(message.chat.id, message.chat.id)
    # await bot.send_message(message.chat.id, "Успешно!")


@send_status_task_smile()
async def set_attend(message: Message, bot: AsyncTeleBot, user: User, visiting):
    day, month, year = message.text.split(".")

    attend_id: int = await _api.set_visit_user(
        await user.token,
        f"{year}-{month}-{day}",
        visiting=visiting,
        user_id=await user.selectable_user.user_id,
    )
    await _api.confirmation_attend_user(
        await user.token,
        attend_id,
        confirmed=True if await user.role != Roles.student else False,
    )
