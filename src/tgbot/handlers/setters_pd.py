from http import HTTPStatus

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from exceptions import ErrorMessage
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.commands import CommandSequence
from tgbot.states.setter_states import *
from tgbot.services.user import UsersFactory
from tgbot.services.utils.message_tools import send_status_task_smile
from tgbot.services.validators.validate import (
    check_valid_date,
    check_valid_phone,
    check_sql_injection,
    check_valid_email,
    check_group_study,
)
from tgbot.services.validators.validator_handler import bind_validator

_api = APIWorker()


async def init_name_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetName.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите имя: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_sql_injection)
async def set_name(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"name": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_dob_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetDob.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите дату рождения: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_valid_date, msg_err=ErrorMessage.DATE_INVALID_FORMAT)
async def set_dob(message: Message, bot: AsyncTeleBot):
    d, m, y = message.text.split(".")
    resp = await set_attr(message, {"date_of_birth": f"{y}-{m}-{d}"})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_phone_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetPhone.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите номер телефона: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_valid_phone, msg_err=ErrorMessage.PHONE_INVALID_FORMAT)
async def set_phone(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"phone": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_email_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetEmail.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите почту: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_valid_email)
async def set_email(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"email": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_address_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetAddress.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите адрес проживания: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_sql_injection)
async def set_address(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"address": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_institute_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetInstitute.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите институт: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_sql_injection)
async def set_institute(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"institute": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_dos_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetDos.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите направление обучения: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(validator=check_sql_injection)
async def set_dos(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"direction_of_study": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def init_group_study_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetGroupStudy.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите группу обучения: ")


@send_status_task_smile(send_ok_status_smile=False)
@bind_validator(
    validator=check_group_study, msg_err=ErrorMessage.GROUP_STUDY_INVALID_FORMAT
)
async def set_group_study(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"group_study": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def check_status(pred: bool, bot, message):
    if pred:
        await bot.send_message(message.chat.id, "Успешно.")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(
            message.chat.id,
            f"Ошибка. Попробуйте ещё раз. "
            f"Или отмените действие с помощью /{CommandSequence.CANCEL}",
        )


async def set_attr(message: Message, attrs: dict):
    user = await UsersFactory().get_user(message)

    result: dict = {"id": await user.user_id, "data": attrs}
    return await _api.set_user_attr(await user.token, result)
