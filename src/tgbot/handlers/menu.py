import asyncio
from http import HTTPStatus

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import Roles
from tgbot.commands import CommandSequence
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.platoon_buttons import PlatoonButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.user import User
from tgbot.utils.callback_data import CallBackData, CallBackStackWorker

_call_back_stack = CallBackStackWorker()


@_call_back_stack.listen_call(is_root=True)
async def menu_handler(message: Message, bot: AsyncTeleBot):
    user = await User(message.from_user.id).ainit()
    role = await user.role

    keyboard = None

    if role == Roles.student:
        keyboard = Student().menu()
    elif role == Roles.squad_commander:
        keyboard = SquadCommander().menu()
    elif role == Roles.platoon_commander:
        keyboard = PlatoonCommander().menu()

    if keyboard is not None:
        message = await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)
    else:
        message = await bot.send_message(message.chat.id, "Для Вашей роли меню ещё не добавлено.")

    _call_back_stack.set_root_id(message.chat.id, message)


@_call_back_stack.listen_call()
async def student_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = Student().menu({"Назад": CallBackData.BACK})

    await send_buttons(call, bot, 'Меню студента', keyboard)


@_call_back_stack.listen_call()
async def squad_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = SquadCommander().menu({"Назад": CallBackData.BACK})

    await send_buttons(call, bot, "Меню командира отделения", keyboard)


@_call_back_stack.listen_call()
async def platoon_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PlatoonButtons().menu()

    await send_buttons(call, bot, "Меню командира взвода", keyboard)


@_call_back_stack.listen_call()
async def marks_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = MarksButtons([1, 2, 3]).menu()

    await send_buttons(call, bot, "Оценки", keyboard)


@_call_back_stack.listen_call()
async def personal_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PersonalDataButtons().menu()

    await send_buttons(call, bot, "Персональные данные", keyboard)


async def attend_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.send_message(call.message.chat.id, 'Посещаемость топ епт')


async def send_buttons(call: CallbackQuery, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    await bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
    )


async def back(call: CallbackQuery, bot: AsyncTeleBot):
    chat_id = call.message.chat.id
    callback_obj = _call_back_stack.get_last_call(chat_id)

    if callback_obj is not None:
        func, (metadata, bot_, _, is_root) = callback_obj.popitem()

        if is_root:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=_call_back_stack.get_root_id(chat_id))

        if asyncio.iscoroutinefunction(func):
            return await func(metadata, bot_)
        else:
            return func(metadata, bot_)

    await bot.send_message(
        chat_id,
        f"Нечего отменять. Стек пуст. Попробуйте: /{CommandSequence.MENU}"
    )
