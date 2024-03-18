from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from exceptions import FunctionStackEmpty, StackRoot
from tgbot.handlers.menu.callback_stack import StackStrider
from tgbot.handlers.menu.inline_menu import self_menu, function_stack, collector, send_marks
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.commands import CommandSequence
from tgbot.services.user import User, UsersFactory
from tgbot.services.utils.message_tools import get_message
from tgbot.services.utils.callback_data import CallBackData


async def callback_handler(call: CallbackQuery, bot: AsyncTeleBot):
    message: Message = get_message(call)
    user: User = await UsersFactory().get_user(message)
    strider = StackStrider(function_stack, collector)
    api = APIWorker()

    if call.data == CallBackData.BACK:
        try:
            await strider.back(message.chat.id, message.message_id)
        except StackRoot as _:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except FunctionStackEmpty as _:
            await bot.send_message(
                message.chat.id,
                f"История пуста. Попробуйте открыть меню ещё раз: /{CommandSequence.MENU}")
    elif call.data == CallBackData.STUDENT_MENU:
        await self_menu(message, bot)
    elif call.data == CallBackData.MARK:
        await send_marks(message, bot, user)
