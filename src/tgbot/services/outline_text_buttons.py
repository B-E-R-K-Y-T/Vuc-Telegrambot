from tgbot.services.collector_fields import CollectorField


class OutlineKeyboardCommand(str):
    pass


class OutlineKeyboardButtons(CollectorField):
    field_type = OutlineKeyboardCommand


class OutlineKeyboardButton(OutlineKeyboardButtons):
    REGISTRATION: OutlineKeyboardCommand = "Регистрация 📝"

    LOGIN: OutlineKeyboardCommand = "Войти 🔑"
    LOGOUT: OutlineKeyboardCommand = "Выйти 🚪"

    MENU: OutlineKeyboardCommand = "Меню 📋"
    QUESTIONS: OutlineKeyboardCommand = "FAQ ❓"

    INFO: OutlineKeyboardCommand = "О ВУЦ ℹ️"
    INCOMING: OutlineKeyboardCommand = "Поступающим 🎓"
    SCHEDULE: OutlineKeyboardCommand = "Расписание 📅"
    CONTACTS: OutlineKeyboardCommand = "Контакты 📞"
    ENTRANCE: OutlineKeyboardCommand = "Алгоритм поступления 🧩"

    CANCEL: OutlineKeyboardCommand = "Отмена ❌"
    BACK: OutlineKeyboardCommand = "Назад 🔙"
