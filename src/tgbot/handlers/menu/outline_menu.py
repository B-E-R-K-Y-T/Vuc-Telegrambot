from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from tgbot.handlers.cancel import cancel_state
from tgbot.handlers.menu.inline_menu import menu_handler
from tgbot.handlers.login import login_handler_init
from tgbot.handlers.logout import logout_handler
from tgbot.services.message_scenarios.scenarios_handler import run_scenario
from tgbot.services.message_scenarios.scenarios import MessageScenarios
from tgbot.services.outline_text_buttons import OutlineKeyboardButton
from tgbot.services.user import UsersFactory


async def create_start_outline_menu_handler() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        row_width=3, one_time_keyboard=True, resize_keyboard=True
    )

    buttons = (
        KeyboardButton(OutlineKeyboardButton.REGISTRATION),
        KeyboardButton(OutlineKeyboardButton.LOGIN),
        KeyboardButton(OutlineKeyboardButton.QUESTIONS),
        KeyboardButton(OutlineKeyboardButton.CANCEL),
    )

    markup.add(*buttons)

    return markup


async def create_authorized_outline_menu_handler() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        row_width=3, one_time_keyboard=True, resize_keyboard=True
    )

    buttons = (
        KeyboardButton(OutlineKeyboardButton.LOGOUT),
        KeyboardButton(OutlineKeyboardButton.MENU),
        KeyboardButton(OutlineKeyboardButton.QUESTIONS),
        KeyboardButton(OutlineKeyboardButton.CANCEL),
    )

    markup.add(*buttons)

    return markup


async def create_outline_menu_questions_handler() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        row_width=2, one_time_keyboard=True, resize_keyboard=True
    )

    buttons = (
        KeyboardButton(OutlineKeyboardButton.INFO),
        KeyboardButton(OutlineKeyboardButton.CONTACTS),
        KeyboardButton(OutlineKeyboardButton.ENTRANCE),
        KeyboardButton(OutlineKeyboardButton.INCOMING),
        KeyboardButton(OutlineKeyboardButton.SCHEDULE),
        KeyboardButton(OutlineKeyboardButton.BACK),
    )

    markup.add(*buttons)

    return markup


async def check_login(message: Message) -> bool:
    user = await UsersFactory().get_user(message)

    if await user.token is None:
        return False
    else:
        return True


async def handle_outline_output(message: Message, bot: AsyncTeleBot):
    text = message.text
    chat_id = message.chat.id

    if text == OutlineKeyboardButton.LOGIN:
        await login_handler_init(message, bot)
    elif text == OutlineKeyboardButton.MENU:
        if await check_login(message):
            await menu_handler(message, bot)
        else:
            await bot.send_message(
                chat_id,
                "Ошибка доступа.",
                reply_markup=await create_start_outline_menu_handler(),
            )

    elif text == OutlineKeyboardButton.QUESTIONS:
        markup = await create_outline_menu_questions_handler()
        await bot.send_message(chat_id, "Что Вас интересует?", reply_markup=markup)
    elif text == OutlineKeyboardButton.LOGOUT:
        markup = await create_start_outline_menu_handler()
        await bot.send_message(chat_id, "Выходим...", reply_markup=markup)
        await logout_handler(message, bot)

    elif text == OutlineKeyboardButton.INCOMING:
        await run_scenario(message, bot, MessageScenarios.INCOMING)

    elif text == OutlineKeyboardButton.CONTACTS:
        await run_scenario(message, bot, MessageScenarios.CONTACTS)

    elif text == OutlineKeyboardButton.SCHEDULE:
        await run_scenario(message, bot, MessageScenarios.SCHEDULE)

    elif text == OutlineKeyboardButton.ENTRANCE:
        await run_scenario(message, bot, MessageScenarios.ENTRANCE)

    elif text == OutlineKeyboardButton.INFO:
        await run_scenario(message, bot, MessageScenarios.INFO)

    elif text == OutlineKeyboardButton.CANCEL:
        await cancel_state(message, bot)

    elif text == OutlineKeyboardButton.REGISTRATION:
        await bot.send_message(
            chat_id,
            "В настоящий момент регистрация отсутствует. "
            "Обратитесь к администратору",
        )

    elif text == OutlineKeyboardButton.BACK:
        if not await check_login(message):
            await bot.send_message(
                chat_id,
                "Принято!",
                reply_markup=await create_start_outline_menu_handler(),
            )
        else:
            await bot.send_message(
                chat_id,
                "Принято!",
                reply_markup=await create_authorized_outline_menu_handler(),
            )
