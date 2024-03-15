import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import Roles
from tgbot.api_worker.client import APIWorker
from tgbot.commands import CommandSequence
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.platoon_buttons import PlatoonButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.user import User
from tgbot.utils.callback_data import CallBackData, CallBackStackWorker
from tgbot.utils.message_tools import send_wait_smile

_api = APIWorker()
_callback_stack = CallBackStackWorker()


@_callback_stack.listen_call(is_root=True)
@send_wait_smile
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

    _callback_stack.set_root_id(message.chat.id, message)


@_callback_stack.listen_call()
async def student_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = Student().menu({"Назад": CallBackData.BACK})

    await send_buttons(call, bot, 'Меню студента', keyboard)


@_callback_stack.listen_call()
async def squad_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = SquadCommander().menu({"Назад": CallBackData.BACK})

    await send_buttons(call, bot, "Меню командира отделения", keyboard)


@_callback_stack.listen_call()
async def platoon_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PlatoonButtons().menu()

    await send_buttons(call, bot, "Меню командира взвода", keyboard)


@_callback_stack.listen_call()
async def marks_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await User(call.message.chat.id).ainit()
    semesters = await _api.get_semesters(user.token, user.user_id)
    keyboard = MarksButtons(semesters).menu()

    await send_buttons(call, bot, "Оценки", keyboard)


@_callback_stack.listen_call()
async def personal_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PersonalDataButtons().menu()

    await send_buttons(call, bot, "Персональные данные", keyboard)


@_callback_stack.go_root
@send_wait_smile
async def attend_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await User(call.message.chat.id).ainit()

    attends = await _api.get_attend(user.token, user.user_id)

    if attends:
        msg = ''

        for attend in attends:
            msg += (f"Дата: {attend["date_v"]}\n"
                    f"Присутствовал: {"Да" if attend["visiting"] else "Нет"}\n"
                    f"Семестр: {attend["semester"]}\n"
                    f"Подтверждено: {"Да" if attend["confirmed"] else "Нет"}\n\n")

        await bot.send_message(call.message.chat.id, msg)
    else:
        await bot.send_message(call.message.chat.id, "Информация отсутствует.")


async def send_buttons(call: CallbackQuery, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    await bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
    )


async def back(call: CallbackQuery, bot: AsyncTeleBot):
    chat_id = call.message.chat.id
    callback_obj = _callback_stack.get_last_call(chat_id)

    if callback_obj is not None:
        func, (metadata, bot_, _, is_root) = callback_obj.popitem()

        if is_root:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=_callback_stack.get_root_id(chat_id)
            )

        if asyncio.iscoroutinefunction(func):
            return await func(metadata, bot_)
        else:
            return func(metadata, bot_)

    await bot.send_message(
        chat_id,
        f"Нечего отменять. Стек пуст. Попробуйте: /{CommandSequence.MENU}"
    )
