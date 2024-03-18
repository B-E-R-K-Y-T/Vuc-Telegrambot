from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.utils.callback_data import CallBackData


class EditAttend(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.ATTEND: CallBackData.ATTEND_VIEW_FROM_COMMANDER,
                TextButton.EDIT_ATTEND: CallBackData.SET_ATTEND,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
