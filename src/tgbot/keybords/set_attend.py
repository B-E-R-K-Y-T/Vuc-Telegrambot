from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.callback_worker.callback_data import CallBackData


class SetAttend(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.POSITIVE_ATTEND: CallBackData.SET_POSITIVE_ATTEND,
                TextButton.NEGATIVE_ATTEND: CallBackData.SET_NEGATIVE_ATTEND,
            },
            *args,
            **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
