from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from exceptions import ErrorMessage
from tgbot.services.utils.message_tools import send_status_task_smile
from tgbot.services.validators.validate import check_valid_date
from tgbot.services.validators.validator_handler import bind_validator


@send_status_task_smile()
@bind_validator(validator=check_valid_date, msg_err=ErrorMessage.DATE_INVALID_FORMAT)
async def set_attend(message: Message, bot: AsyncTeleBot):
    d, m, y = message.text.split(".")
    # resp = await set_attr(message, {"date_of_birth": f"{y}-{m}-{d}"})
    #
    # await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)
