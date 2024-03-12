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

    async def get_id_from_tg(self, token: str, telegram_id: int) -> int:
        resp = await self.request.get('/users/get_id_from_tg',
                                      headers=self.headers,
                                      cookies={'bonds': token},
                                      params={'telegram_id': telegram_id})

        d = await resp.text()
        print(d)

        if resp.status == HTTPStatus.OK.value:
            return (await resp.json())['id']

    async def get_user_role(self, token: str, user_id: int) -> str:
        resp = await self.request.get('/users/get_user_role',
                                      headers=self.headers,
                                      cookies={'bonds': token},
                                      params={'user_id': user_id})

        if resp.status == HTTPStatus.OK.value:
            return (await resp.json())['role']


__all__ = (
    APIWorker.__name__,
)
