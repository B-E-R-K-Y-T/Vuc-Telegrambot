from http import HTTPStatus

from tgbot.api_worker.request import Request


class APIWorker:
    def __init__(self):
        self.request = Request()

    async def login(self, username: str, password: str) -> str:
        """
        Вернет JWT токен в виде строки
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'username': username,
            'password': password
        }

        resp = await self.request.post('/auth/jwt/login', headers=headers, data=data)

        if resp.status == HTTPStatus.NO_CONTENT.value:
            return resp.cookies.get('bonds').value


__all__ = (
    APIWorker.__name__,
)
