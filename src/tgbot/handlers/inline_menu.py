import asyncio
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup

from config import Roles
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
from tgbot.services.utils.callback_data import CallBackData, CallBackStackWorker
from tgbot.services.utils.message_tools import send_status_task_smile, get_message

_api = APIWorker()
_callback_stack = CallBackStackWorker()


@send_status_task_smile(send_ok_status_smile=False)
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
async def switch_user(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    if call.data.isdigit():
        user.selectable_user = await UsersFactory().get_user_by_telegram_id(int(call.data))

    keyboard = EditStudent().menu()
    await send_buttons(call, bot, 'Просмотр студента', keyboard)


@_callback_stack.listen_call()
async def student_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = Student().menu()

    await send_buttons(call, bot, 'Меню студента', keyboard)


@_callback_stack.listen_call()
async def view_squads_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    count_squads = await user.count_squad_in_platoon
    keyboard = Squads(count_squads).menu()

    await send_buttons(call, bot, "Меню командира отделения", keyboard)


@_callback_stack.listen_call()
async def view_squad_menu(call: CallbackQuery, bot: AsyncTeleBot):
    squads_buttons_map = {
        CallBackData.SQUAD_ONE: 1,
        CallBackData.SQUAD_TWO: 2,
        CallBackData.SQUAD_THREE: 3
    }

    await squad_menu(call, bot, squads_buttons_map[call.data])


@_callback_stack.listen_call()
async def squad_commander_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await squad_menu(call, bot)


async def squad_menu(call: CallbackQuery, bot: AsyncTeleBot, squad_number: Optional[int] = None):
    user = await UsersFactory().get_user(call)

    buttons = {}
    squads = {1: [], 2: [], 3: []}

    for student in (await user.get_subordinate_users()).values():
        if await student.role == Roles.student:
            telegram_id = student.telegram_id
            name = await student.name
            squads[await student.squad_number].append({name: telegram_id})

    if squad_number is None:
        squad_number: int = await user.squad_number

    for btn in squads[squad_number]:
        n, u_id = btn.popitem()
        buttons[n] = u_id

    keyboard = Squad().menu(buttons)

    await send_buttons(call, bot, "Меню командира отделения", keyboard)


@_callback_stack.listen_call()
async def platoon_menu(call: CallbackQuery, bot: AsyncTeleBot):
    keyboard = PlatoonButtons().menu()

    await send_buttons(call, bot, "Меню командира взвода", keyboard)


@_callback_stack.listen_call()
async def marks_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)
    user.selectable_user = None

    await marks_menu_build(call, bot, user)


@_callback_stack.listen_call()
async def marks_menu_from_commander(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    await marks_menu_build(call, bot, user)


async def marks_menu_build(call: CallbackQuery, bot: AsyncTeleBot, user: User):
    semesters = await user.semesters
    keyboard = MarksButtons(semesters).menu()

    await send_buttons(call, bot, "Оценки", keyboard)

async def view_marks(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)
    token = await user.token

    if user.selectable_user is not None:
        user = user.selectable_user

    await send_marks(call, bot, user, token)


@send_status_task_smile()
async def send_marks(call: CallbackQuery, bot: AsyncTeleBot, user: User, token: str):
    callback_map = {
        CallBackData.SEMESTER_ONE: 1,
        CallBackData.SEMESTER_TWO: 2,
        CallBackData.SEMESTER_THREE: 3,
        CallBackData.SEMESTER_FOUR: 4,
        CallBackData.SEMESTER_FIVE: 5,
        CallBackData.SEMESTER_SIX: 6,
    }

    marks = await _api.get_marks_by_semester(token, await user.user_id, callback_map.get(call.data))

    msg = ""

    for mark in marks:
        msg += (f"Дата: {mark["mark_date"]}\n"
                f"Тема: {mark["theme"]}\n"
                f"Оценка: {mark["mark"]}\n\n")

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


@send_status_task_smile()
async def view_attend(call: CallbackQuery, bot: AsyncTeleBot):
    user = await UsersFactory().get_user(call)

    attends = await user.attend

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
