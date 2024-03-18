from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.services.api_worker.client import APIWorker
from tgbot.services.user import UsersFactory
from tgbot.services.utils.message_tools import send_status_task_smile


@send_status_task_smile()
async def personal_info(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await UsersFactory().get_user(message)

    token = await user.token
    user_id = await user.user_id

    data = await api.get_self(token, user_id)
    translate_map = {
        "name": "Имя",
        "date_of_birth": "Дата рождения",
        "phone": "Телефон",
        "email": "Почта",
        "address": "Адрес",
        "institute": "Институт",
        "direction_of_study": "Направление обучения",
        "group_study": "Учебная группа",
        "platoon_number": "Номер взвода",
        "squad_number": "Номер отделения",
        "role": "Роль",
    }

    format_data = ""

    for k, v in data.items():
        if k in translate_map:
            format_data += f"🔵 {translate_map[k]}:  {v}\n"

    await bot.send_message(message.chat.id, f"{format_data}")
