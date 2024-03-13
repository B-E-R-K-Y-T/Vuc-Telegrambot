import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from config import Roles
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.user import User
from tgbot.utils.callback_data import CallBackData, CallBackStackWorker

_call_back_stack = CallBackStackWorker()


@_call_back_stack.listen_call
async def menu_handler(message: Message, bot: AsyncTeleBot):
    user = await User(message.from_user.id).ainit()
    role = await user.role

    keyboard = None

    if role == Roles.student:
        keyboard = Student().menu()
    elif role == Roles.squad_commander:
        keyboard = SquadCommander().menu()

    if keyboard is not None:
        await bot.send_message(message.chat.id, f"Главное меню.", reply_markup=keyboard)
    else:
        await bot.send_message(message.chat.id, "Для Вашей роли меню ещё не добавлено.")


@_call_back_stack.listen_call
async def student_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = Student().menu({"Назад": CallBackData.BACK})

    await bot.edit_message_text(
        "Меню студента",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
    )


async def back(call: CallbackQuery, bot: AsyncTeleBot):
    callback_obj = _call_back_stack.get_last_call(call.message.chat.id)

    if callback_obj is not None:
        func, (metadata, bot_) = callback_obj.popitem()

        if asyncio.iscoroutinefunction(func):
            return await func(metadata, bot_)
        else:
            return func(metadata, bot_)

    await bot.send_message(call.message.chat.id, "Нечего отменять.")
