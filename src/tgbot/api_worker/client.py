from http import HTTPStatus

from tgbot.api_worker.request import Request


class APIWorker:
    def __init__(self):
        self.request = Request()
        self.headers = {
            "accept": "application/json",
        }

    async def login(self, username: str, password: str) -> str | None:
        """
        Вернет JWT токен в виде строки
        """
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        data = {
            'username': username,
            'password': password
        }

        resp = await self.request.post('/auth/jwt/login', headers=self.headers, data=data)

        if resp is None:
            return None

        if resp.status == HTTPStatus.NO_CONTENT.value:
            return resp.cookies.get('bonds').value

    async def logout(self, token: str) -> bool:
        resp = await self.request.post('/auth/jwt/logout', headers=self.headers, cookies={'bonds': token})

        if resp.status == HTTPStatus.NO_CONTENT.value:
            return True

        return False


__all__ = (
    APIWorker.__name__,
)
