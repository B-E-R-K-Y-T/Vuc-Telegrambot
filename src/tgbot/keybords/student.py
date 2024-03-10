from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def marks():
    semesters = [1, 2, 3]
    keyboard = InlineKeyboardMarkup(row_width=7)

    for semester in semesters:
        keyboard.add(
            InlineKeyboardButton(
                text=f'Semester {semester}',
                callback_data='2'
            )
        )

    return keyboard
