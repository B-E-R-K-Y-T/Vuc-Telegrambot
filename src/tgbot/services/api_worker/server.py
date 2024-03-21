from typing import Callable, Awaitable

from aiohttp import web


class HttpServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = web.Application()

    def post(self, endpoint: str):
        def decorator(handler: Callable | Awaitable):
            self.app.router.add_post(endpoint, handler)

            return handler

        return decorator

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print(f"Server started at http://{self.host}:{self.port}")
