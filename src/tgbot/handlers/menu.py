import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import Roles
from tgbot.api_worker.client import APIWorker
from tgbot.commands import CommandSequence
from tgbot.handlers.self import self
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.platoon_buttons import PlatoonButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.user import UsersFactory
from tgbot.utils.callback_data import CallBackData, CallBackStackWorker
from tgbot.utils.message_tools import send_wait_smile, get_message

_api = APIWorker()
_callback_stack = CallBackStackWorker()


@send_wait_smile
@_callback_stack.listen_call(is_root=True)
async def menu_handler(message: Message, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(message)
    role = await user.role

    keyboard = None

    if role == Roles.student:
        keyboard = Student(reopen_menu_button_on=False, back_button_on=False).menu()
    elif role == Roles.squad_commander:
        keyboard = SquadCommander(reopen_menu_button_on=False, back_button_on=False).menu()
    elif role == Roles.platoon_commander:
        keyboard = PlatoonCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    if keyboard is not None:
        message = await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)
    else:
        message = await bot.send_message(message.chat.id, "Для Вашей роли меню ещё не добавлено.")

    _callback_stack.set_root_id(message.chat.id, message)


@_callback_stack.listen_call()
async def student_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = Student().menu()

    await send_buttons(call, bot, 'Меню студента', keyboard)


@_callback_stack.listen_call()
async def squad_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    buttons = {}

    if not user.get_subordinate_users():

        platoon_number = await user.platoon_number
        squad_number = await user.squad_number
        students = await _api.get_students_by_squad(await user.token, platoon_number, squad_number)

        for student in students:
            if student["role"] == Roles.student:
                user_id = student.pop("id")

                buttons[student["name"]] = user_id
                student["user_id"] = user_id

                await user.add_subordinate_user(UsersFactory().create_user(student))
    else:
        for student in user.get_subordinate_users().values():
            if await student.role == Roles.student:
                user_id = await student.user_id
                name = await student.name

                buttons[name] = user_id

    keyboard = SquadCommander().menu(buttons)

    await send_buttons(call, bot, "Меню командира отделения", keyboard)


@_callback_stack.listen_call()
async def platoon_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PlatoonButtons().menu()

    await send_buttons(call, bot, "Меню командира взвода", keyboard)


@_callback_stack.listen_call()
async def marks_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)
    semesters = await _api.get_semesters(await user.token, await user.user_id)
    keyboard = MarksButtons(semesters).menu()

    await send_buttons(call, bot, "Оценки", keyboard)


@send_wait_smile
async def send_marks(call: CallbackQuery, bot: AsyncTeleBot):
    callback_map = {
        CallBackData.SEMESTER_ONE: 1,
        CallBackData.SEMESTER_TWO: 2,
        CallBackData.SEMESTER_THREE: 3,
        CallBackData.SEMESTER_FOUR: 4,
        CallBackData.SEMESTER_FIVE: 5,
        CallBackData.SEMESTER_SIX: 6,
    }

    user = await UsersFactory().get_user(call)

    attends = await _api.get_marks_by_semester(await user.token, await user.user_id, callback_map.get(call.data))

    msg = ""

    for attend in attends:
        msg += (f"Дата: {attend["mark_date"]}\n"
                f"Тема: {attend["theme"]}\n"
                f"Оценка: {attend["mark"]}\n\n")

    await bot.send_message(call.message.chat.id, msg)


@_callback_stack.listen_call()
async def personal_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PersonalDataButtons().menu()

    await send_buttons(call, bot, "Персональные данные", keyboard)


async def reopen_menu(call: CallbackQuery, bot: AsyncTeleBot):
    message = get_message(call)

    await bot.delete_message(message.chat.id, message.message_id)
    await menu_handler(message, bot)


async def view_pd(call: CallbackQuery, bot: AsyncTeleBot):
    await self(get_message(call), bot)


@send_wait_smile
async def attend_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    attends = await _api.get_attend(await user.token, await user.user_id)

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


async def send_buttons(metadata: Message | CallbackQuery, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    message = get_message(metadata)

    await bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
    )


async def back(call: CallbackQuery, bot: AsyncTeleBot):
    chat_id = call.message.chat.id
    callback_obj = _callback_stack.get_last_call(chat_id)

    if callback_obj is not None:
        func, (metadata, bot_, _, is_root) = callback_obj.popitem()

        message = get_message(metadata)

        if is_root:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=_callback_stack.get_root_id(message.chat.id)
            )

        if asyncio.iscoroutinefunction(func):
            return await func(metadata, bot_)
        else:
            return func(metadata, bot_)

    await bot.send_message(
        chat_id,
        f"Нечего отменять. Стек пуст. Попробуйте: /{CommandSequence.MENU}, чтобы вернуться в начало."
    )
