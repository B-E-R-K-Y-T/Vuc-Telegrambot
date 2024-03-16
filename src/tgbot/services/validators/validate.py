import re

from telebot.types import Message


async def check_valid_email(message: Message) -> bool:
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$"

    return bool(re.search(pattern, message.text))


async def check_valid_date(message: Message) -> bool:
    pattern = r"^\d{1,2}\.\d{1,2}\.\d{4}$"

    return bool(re.search(pattern, message.text))


async def check_valid_phone(message: Message) -> bool:
    pattern = r"^(?:\+7|8|8800)[\s(-]*?\d{3}[\s)-]*?\d{3}[\s-]*?\d{2}[\s-]*?\d{2}$"

    return bool(re.search(pattern, message.text))


async def check_sql_injection(message: Message) -> bool:
    """
    Спасет от простых SQL-инъекций
    """
    pattern = r"^[^';]*$"

    return bool(
        re.search(pattern, message.text)
        and not any(
            op in message.text.upper()
            for op in ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"]
        )
    )


async def check_group_study(message: Message) -> bool:
    pattern = r"^[А-Яа-я]{1,4}-\d{2}-\d{2}$"

    return bool(re.search(pattern, message.text))
