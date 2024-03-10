from telebot.asyncio_handler_backends import StatesGroup, State


class Login(StatesGroup):
    name = State()
    password = State()
