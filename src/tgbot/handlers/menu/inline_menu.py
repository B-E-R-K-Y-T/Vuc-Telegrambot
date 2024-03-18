from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, InlineKeyboardMarkup

from config import Roles
from tgbot.handlers.self import personal_info
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.squad import Squad
from tgbot.keybords.squads import Squads
from tgbot.services.callback_worker.callback_stack import CallbackStackBuilder, CallFunctionStack
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.services.user import UsersFactory, User
from tgbot.services.utils.message_tools import send_status_task_smile

function_stack = CallFunctionStack()
stack_builder = CallbackStackBuilder(function_stack)


@send_status_task_smile(send_ok_status_smile=False)
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


@stack_builder.root
async def student_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = Student(reopen_menu_button_on=False, back_button_on=False).menu()

    await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@stack_builder.listen_call
async def view_squads_menu(message: Message, bot: AsyncTeleBot, user: User):
    count_squads = await user.count_squad_in_platoon
    keyboard = Squads(count_squads).menu()

    await edit_menu(message, bot, "Меню командира отделения", keyboard)


@stack_builder.listen_call
async def view_squad_menu(message: Message, bot: AsyncTeleBot, user: User, squad_num: int):
    await squad_menu(message, bot, user, squad_num)


@stack_builder.listen_call
async def squad_menu(message: Message, bot: AsyncTeleBot, user: User, squad_number: Optional[int] = None):
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

    await edit_menu(message, bot, "Меню командира отделения", keyboard)


@stack_builder.root
async def squad_commander_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = SquadCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@stack_builder.root
async def platoon_commander_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = PlatoonCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    return await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@stack_builder.listen_call
async def self_menu(message: Message, bot: AsyncTeleBot):
    keyboard = Student().menu()

    await edit_menu(message, bot, f"Меню студента", keyboard=keyboard)


@stack_builder.listen_call
async def semesters_menu(message: Message, bot: AsyncTeleBot, user: User):
    keyboard = MarksButtons(await user.semesters).menu()

    await edit_menu(message, bot, "Семестры", keyboard=keyboard)


@send_status_task_smile()
async def send_marks(message: Message, bot: AsyncTeleBot, user: User, semester: int):
    marks = await user.get_marks(semester)

    msg = ""

    for mark in marks:
        msg += (f"Дата: {mark["mark_date"]}\n"
                f"Тема: {mark["theme"]}\n"
                f"Оценка: {mark["mark"]}\n\n")

    await bot.send_message(message.chat.id, msg)


@stack_builder.listen_call
async def personal_menu(message: Message, bot: AsyncTeleBot):
    keyboard = PersonalDataButtons().menu()

    await edit_menu(message, bot, "Персональные данные", keyboard)


@send_status_task_smile()
async def view_attend(message: Message, bot: AsyncTeleBot, user: User):
    attends = await user.attend

    if attends:
        msg = ''

        for attend in attends:
            msg += (f"Дата: {attend["date_v"]}\n"
                    f"Присутствовал: {"Да" if attend["visiting"] else "Нет"}\n"
                    f"Семестр: {attend["semester"]}\n"
                    f"Подтверждено: {"Да" if attend["confirmed"] else "Нет"}\n\n")

        await bot.send_message(message.chat.id, msg)
    else:
        await bot.send_message(message.chat.id, "Информация отсутствует.")


async def send_personal_info(message: Message, bot: AsyncTeleBot):
    await personal_info(message, bot)


async def edit_menu(message: Message, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    await bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
    )
