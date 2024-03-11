import time

from tgbot.utils.database import Database


class User:
    def __init__(self, tg_id: int):
        self.tg_id: int = tg_id
        self.__username = None
        self.__password = None
        self.db = Database()

    async def get_jwt(self) -> str | None:
        now = time.time()
        jwt = await self.db.get_value(key=str(self.tg_id))

        if jwt is None:
            return None
        else:
            date, token = jwt.decode('utf-8').split(',')

            if now - int(date) > 3600:
                await self.db.del_value(key=str(self.tg_id))
                return None

            return token

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value
