from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.utils.callback_data import CallBackData


class Student(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.MARKS: CallBackData.MARK,
                TextButton.ATTEND: CallBackData.ATTEND,
                TextButton.PERSONAL_DATA: CallBackData.PERSONAL_DATA,
                TextButton.EDIT_PERSONAL_DATA: CallBackData.EDIT_PERSONAL_DATA,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
