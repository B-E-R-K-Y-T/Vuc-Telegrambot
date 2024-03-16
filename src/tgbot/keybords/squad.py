from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard


class Squad(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
