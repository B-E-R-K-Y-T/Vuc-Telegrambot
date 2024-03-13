import re

from telebot.types import Message


async def check_valid_email(message: Message) -> bool:
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$"

    if re.fullmatch(pattern, message.text):
        return True
    else:
        return False
