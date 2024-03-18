import asyncio
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import Roles
from tgbot.handlers.menu.callback_stack import CallbackCollector, CallFunctionStack
from tgbot.keybords.edit_student import EditStudent
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.commands import CommandSequence
from tgbot.handlers.self import self
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.platoon_buttons import PlatoonButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad import Squad
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.squads import Squads
from tgbot.keybords.student import Student
from tgbot.services.user import UsersFactory, User
from tgbot.services.utils.callback_data import CallBackData
from tgbot.services.utils.message_tools import send_status_task_smile, get_message

function_stack = CallFunctionStack()
collector = CallbackCollector(function_stack)


# @send_status_task_smile(send_ok_status_smile=False)
async def menu_handler(message: Message, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(message)
    role = await user.role

    if role == Roles.student:
        await student_start_menu(message, bot)
    elif role == Roles.squad_commander:
        await squad_commander_start_menu(message, bot)
    elif role == Roles.platoon_commander:
        await platoon_commander_start_menu(message, bot)
    else:
        await bot.send_message(message.chat.id, "Для Вашей роли нет меню.")


@collector.root
async def student_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = Student(reopen_menu_button_on=False, back_button_on=False).menu()

    await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@collector.root
async def squad_commander_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = SquadCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@collector.root
async def platoon_commander_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = PlatoonCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    return await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@collector.listen_call
async def self_menu(message: Message, bot: AsyncTeleBot):
    keyboard = Student().menu()

    await edit_menu(message, bot, f"Меню студента", keyboard=keyboard)


@send_status_task_smile()
async def send_marks(message: Message, bot: AsyncTeleBot, api: APIWorker):
    pass


async def edit_menu(message: Message, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    await bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
    )
