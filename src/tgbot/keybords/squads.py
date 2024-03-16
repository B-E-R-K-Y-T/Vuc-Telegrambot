from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class Squads(BaseKeyboard):
    def __init__(self, count_squads: int, *args, **kwargs):
        super().__init__(
            *args, **kwargs
        )
        self.count_squads: int = count_squads

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        squads_buttons_map = {
            1: CallBackData.SQUAD_ONE,
            2: CallBackData.SQUAD_TWO,
            3: CallBackData.SQUAD_THREE
        }

        for squad_num in range(1, self.count_squads + 1):
            self.buttons[f"Отделение {squad_num}"] = squads_buttons_map[squad_num]

        return self.build_keyboard(self.buttons)
