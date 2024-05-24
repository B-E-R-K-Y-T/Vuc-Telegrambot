from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, InlineKeyboardMarkup

from config import Roles
from tgbot.handlers.self import personal_info
from tgbot.keybords.edit_attend import EditAttend
from tgbot.keybords.edit_student import EditStudent
from tgbot.keybords.personal_data import PersonalDataButtons
from tgbot.keybords.platoon_menu_settings import PlatoonSettingsMenu
from tgbot.keybords.set_attend import SetAttend
from tgbot.keybords.squad import Squad
from tgbot.keybords.squads import Squads
from tgbot.services.callback_worker.callback_data import CallBackPrefix
from tgbot.services.callback_worker.callback_stack import CallbackStackBuilder, CallFunctionStack
from tgbot.keybords.marks import MarksButtons
from tgbot.keybords.platoon_commander import PlatoonCommander
from tgbot.keybords.squad_commander import SquadCommander
from tgbot.keybords.student import Student
from tgbot.services.user import UsersFactory, User, UserStates
from tgbot.services.utils.message_tools import send_status_task_smile
from tgbot.states.attend import PositiveAttend, NegativeAttend

function_stack = CallFunctionStack()
stack_builder = CallbackStackBuilder(function_stack)


# @send_status_task_smile(send_success_status_smile=False)
async def menu_handler(message: Message, bot: AsyncTeleBot):
    current_user = await UsersFactory().get_user(message)
    current_user.clear_state()

    role = await current_user.role

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

    return await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


@stack_builder.listen_call
async def view_squads_menu(message: Message, bot: AsyncTeleBot, user: User):
    count_squads = await user.count_squad_in_platoon
    keyboard = Squads(count_squads).menu()

    user.clear_state()
    await edit_menu(message, bot, "Меню командира отделения", keyboard)


@stack_builder.listen_call
async def view_platoon_menu(message: Message, bot: AsyncTeleBot):
    keyboard = PlatoonSettingsMenu().menu()

    await edit_menu(message, bot, "Меню командира взвода", keyboard)


@stack_builder.listen_call
async def view_squad_menu(message: Message, bot: AsyncTeleBot, user: User, squad_num: int):
    user.set_state(UserStates.WORK_SELECTED_USER)
    await squad_menu(message, bot, user, squad_num)


@stack_builder.listen_call
async def mark_view_from_student_to_commander(message: Message, bot: AsyncTeleBot, selectable_user: User):
    semesters: list = await selectable_user.semesters

    keyboard = MarksButtons(semesters).menu()

    await edit_menu(message, bot, "Оценки студента", keyboard=keyboard)


async def squad_menu(message: Message, bot: AsyncTeleBot, user: User, squad_number: Optional[int] = None):
    buttons = {}
    squads = {1: [], 2: [], 3: []}

    for student in (await user.get_subordinate_users()).values():
        if await student.role == Roles.student:
            user_id = await student.user_id
            name = await student.name
            squads[await student.squad_number].append({name: user_id})

    if squad_number is None:
        squad_number: int = await user.squad_number

    for btn in squads[squad_number]:
        name, user_id = btn.popitem()
        buttons[name] = f"{CallBackPrefix.EDIT_STUDENT}{user_id}"

    keyboard = Squad().menu(buttons)

    await edit_menu(message, bot, "Меню командира отделения", keyboard)


@stack_builder.root
async def squad_commander_start_menu(message: Message, bot: AsyncTeleBot):
    keyboard = SquadCommander(reopen_menu_button_on=False, back_button_on=False).menu()

    return await bot.send_message(message.chat.id, f"Главное меню", reply_markup=keyboard)


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

    msg = f"Оценки студента: {await user.name}\n\n"

    for mark in marks:
        msg += (f"Дата: {mark["mark_date"]}\n"
                f"Тема: {mark["theme"]}\n"
                f"Оценка: {mark["mark"]}\n\n")

    if not marks:
        msg += "Отсутствуют."

    await bot.send_message(message.chat.id, msg)


@stack_builder.listen_call
async def personal_menu(message: Message, bot: AsyncTeleBot):
    keyboard = PersonalDataButtons().menu()

    await edit_menu(message, bot, "Персональные данные", keyboard)


@stack_builder.listen_call
async def edit_attend(message: Message, bot: AsyncTeleBot):
    keyboard = EditAttend().menu()

    await edit_menu(message, bot, "Посещаемость", keyboard)


@stack_builder.listen_call
async def edit_student_from_commander(message: Message, bot: AsyncTeleBot):
    keyboard = EditStudent().menu()

    await edit_menu(message, bot, "Просмотр студента", keyboard)


@send_status_task_smile()
async def view_attend(message: Message, bot: AsyncTeleBot, user: User):
    attends = await user.attend
    msg = f"Посещаемость студента: {await user.name}\n\n"

    attend_mode = {
        0: "не был",
        1: "был",
        2: "наряд",
        3: "командировка",
        4: "болезнь"
    }

    for attend in attends:
        msg += (f"Дата: {attend["date_v"]}\n"
                f"Заверено: {attend_mode[attend["visiting"]]}\n"
                f"Семестр: {attend["semester"]}\n"
                f"Заверено: {"Да" if attend["confirmed"] else "Нет"}\n\n")

    if not attends:
        msg += "Информация отсутствует."

    await bot.send_message(message.chat.id, msg)


@stack_builder.listen_call
async def set_attend_menu(message: Message, bot: AsyncTeleBot):
    keyboard = SetAttend().menu()

    await edit_menu(message, bot, "Отметить присутствие", keyboard)


async def set_positive_attend_state(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Напишите дату: ")
    await bot.set_state(message.chat.id, PositiveAttend.init, message.chat.id)


async def set_negative_attend_state(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Напишите дату: ")
    await bot.set_state(message.chat.id, NegativeAttend.init, message.chat.id)


async def send_personal_info(message: Message, bot: AsyncTeleBot):
    await personal_info(message, bot)


async def edit_menu(message: Message, bot: AsyncTeleBot, text: str, keyboard: InlineKeyboardMarkup):
    await bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        reply_markup=keyboard,
    )
