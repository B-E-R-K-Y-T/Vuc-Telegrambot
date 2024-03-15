import re

from telebot.types import Message


def _validate(pred):
    if pred:
        return True
    else:
        return False


async def check_valid_email(message: Message) -> bool:
    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$"

    return _validate(re.search(pattern, message.text))


async def check_valid_date(message: Message) -> bool:
    pattern = r"^\d{1,2}\.\d{1,2}\.\d{4}$"

    return _validate(re.search(pattern, message.text))


async def check_valid_phone(message: Message) -> bool:
    pattern = r"^(?:\+7|8|8800)[\s(-]*?\d{3}[\s)-]*?\d{3}[\s-]*?\d{2}[\s-]*?\d{2}$"

    return _validate(re.search(pattern, message.text))


async def check_sql_injection(message: Message) -> bool:
    """
    Спасет от простых SQL-инъекций
    """
    pattern = r"^[^';]*$"

    return _validate(
        re.search(pattern, message.text)
        and not any(
            op in message.text.upper()
            for op in ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"]
        )
    )


async def check_group_study(message: Message) -> bool:
    pattern = r"^[А-Яа-я]{1,4}-\d{2}-\d{2}$"

    return _validate(re.search(pattern, message.text))
