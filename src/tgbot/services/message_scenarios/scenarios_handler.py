import asyncio
import os
from typing import Optional, BinaryIO

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

__TARGET__ = "."


class NextMessage:
    pass


class InitScenario:
    pass


class TextMessage:
    def __init__(self, text: str):
        self.text: str = text

    def __str__(self):
        return self.text


class Sleep:
    def __init__(self, seconds: float = 0.5):
        self.seconds: float = seconds

    async def sleep(self):
        await asyncio.sleep(self.seconds)


class Photo:
    """
    Фотографии для сценариев надо класть сюда:

    /src/data/message_scenario_photo/
    """

    def __init__(self, path: str):
        self.__path: str = path

    @property
    def photo(self) -> BinaryIO:
        return open(
            f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))}"
            f"/data/message_scenario_photo/{self.__path}",
            "rb",
        )


async def run_scenario(message: Message, bot: AsyncTeleBot, scenario: tuple):
    if not isinstance(scenario, tuple):
        raise ValueError("Scenario must be a tuple")

    chat_id: int = message.chat.id
    msg_scar: Optional[Message] = None
    text = __TARGET__

    for step in scenario:
        if isinstance(step, InitScenario) or isinstance(step, NextMessage):
            text = __TARGET__
            msg_scar = await bot.send_message(chat_id, text)

            continue
        elif isinstance(step, TextMessage):
            text += "\n" + str(step) + "\n"
            await bot.edit_message_text(text, msg_scar.chat.id, msg_scar.message_id)
        elif isinstance(step, Sleep):
            await step.sleep()
        elif isinstance(step, Photo):
            try:
                await bot.send_photo(chat_id, step.photo)
            except FileNotFoundError as _:
                await bot.send_message(chat_id, "❗️Photo not found❗️")
        else:
            raise TypeError(f"Unexpected type {type(step)}")

        text = text.replace(__TARGET__, "")

    await bot.edit_message_text(text, msg_scar.chat.id, msg_scar.message_id)
