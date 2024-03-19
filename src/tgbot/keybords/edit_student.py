from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.callback_worker.callback_data import CallBackData


class EditStudent(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.MARKS: CallBackData.MARK_VIEW_FROM_STUDENT_TO_COMMANDER,
                TextButton.ATTEND: CallBackData.EDIT_ATTEND_OF_STUDENT,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
