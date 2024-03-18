from telebot.asyncio_handler_backends import StatesGroup, State


class Attend(StatesGroup):
    init = State()
