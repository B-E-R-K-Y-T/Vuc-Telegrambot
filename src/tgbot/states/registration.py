from telebot.asyncio_handler_backends import StatesGroup, State


class Registration(StatesGroup):
    token = State()
