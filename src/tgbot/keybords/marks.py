from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.services.utils.callback_data import CallBackData


class MarksButtons(BaseKeyboard):
    def __init__(self, semesters: list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.semesters: list = semesters

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        callback_map = {
            1: CallBackData.SEMESTER_ONE,
            2: CallBackData.SEMESTER_TWO,
            3: CallBackData.SEMESTER_THREE,
            4: CallBackData.SEMESTER_FOUR,
            5: CallBackData.SEMESTER_FIVE,
            6: CallBackData.SEMESTER_SIX,
        }

        semester_buttons = {}

        for semester in self.semesters:
            name = f"{semester} Семестр"
            semester_buttons[name] = callback_map.get(semester)

        self.update_buttons(semester_buttons)

        return self.build_keyboard(self.buttons)
