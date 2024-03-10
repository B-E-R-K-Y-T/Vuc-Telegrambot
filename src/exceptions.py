from telebot.async_telebot import ExceptionHandler

from logger import LOGGER


class VucExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        LOGGER.err(exception)
