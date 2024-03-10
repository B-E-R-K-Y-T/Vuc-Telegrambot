from abc import ABC, abstractmethod

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class BaseKeyboard(ABC):
    row_width: int = 3

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)

        return self(*args, **kwargs)

    def __init__(self, callback_data: str | None = None):
        self.callback_data = callback_data
        self.keyboard = InlineKeyboardMarkup(row_width=self.row_width)

    @abstractmethod
    def build_keyboard(self) -> InlineKeyboardButton:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, *args, **kwargs) -> InlineKeyboardButton:
        raise NotImplementedError

