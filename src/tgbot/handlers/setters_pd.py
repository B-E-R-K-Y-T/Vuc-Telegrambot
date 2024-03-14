import json
from http import HTTPStatus
from pprint import pprint

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.api_worker.client import APIWorker
from tgbot.commands import CommandSequence
from tgbot.user import User
from tgbot.states.set_name import SetName


_api = APIWorker()


async def init_name_state(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.set_state(call.message.chat.id, SetName.init, call.message.chat.id)
    await bot.send_message(call.message.chat.id, "Введите имя: ")


async def set_name(message: Message, bot: AsyncTeleBot):
    resp = await set_attr(message, {"name": message.text})

    await check_status(resp.status == HTTPStatus.NO_CONTENT.value, bot, message)


async def check_status(pred: bool, bot, message):
    if pred:
        await bot.send_message(message.chat.id, "Успешно.")
        await bot.delete_state(message.from_user.id, message.chat.id)
    else:
        await bot.send_message(message.chat.id,
                               f"Ошибка. Попробуйте ещё раз. Или отмените действие с помощью /{CommandSequence.CANCEL}")


async def set_attr(message: Message, attrs: dict):
    user = await User(message.from_user.id).ainit()
    token = await user.get_jwt()
    user_id = await _api.get_id_from_email(token, await user.get_email())

    result: dict = {"id": user_id, "data": attrs}
    return await _api.set_user_attr(token, result)

