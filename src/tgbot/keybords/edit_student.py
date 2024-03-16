from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.utils.callback_data import CallBackData


class EditStudent(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.MARKS: CallBackData.MARK_VIEW_FROM_COMMADER,
                TextButton.ATTEND: CallBackData.EDIT_ATTEND,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
