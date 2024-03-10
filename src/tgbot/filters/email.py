import re

from telebot.asyncio_filters import SimpleCustomFilter


class EmailFilter(SimpleCustomFilter):
    """
    Filter for email str
    """

    key = "email_check"

    async def check(self, message):
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$'

        return True if re.fullmatch(pattern, message.text) else False
