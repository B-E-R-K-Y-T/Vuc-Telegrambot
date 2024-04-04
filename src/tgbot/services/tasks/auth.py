from functools import wraps
from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.abc import Request

from config import app_settings
from tgbot.services.utils.util import sync_async_call


def authenticate(func: Callable | Awaitable):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        json_data = await request.json()
        auth_token = json_data.get('auth_token')

        if auth_token == app_settings.TOKEN:
            return await sync_async_call(func, request, *args, **kwargs)
        else:
            return web.HTTPForbidden()

    return wrapper
