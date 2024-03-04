from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.async_telebot import CancelUpdate


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit, bot) -> None:
        super().__init__()
        self.last_time = {}
        self.limit = limit
        self.update_types = ["message"]
        self.bot = bot
        # Всегда укажите типы обновлений, иначе middleware не будет работать

    async def pre_process(self, message, data):
        if message.text != "/spam":
            return  # сделаем его активным только для этой команды
        if not message.from_user.id in self.last_time:
            # Пользователь отсутствует в словаре, давайте добавим и отменим это действие
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            # Пользователь флудит
            await self.bot.send_message(
                message.chat.id, "Вы отправляете запросы слишком часто"
            )
            return CancelUpdate()
        # записываем время последнего запроса
        self.last_time[message.from_user.id] = message.date

    async def post_process(self, message, data, exception):
        pass
