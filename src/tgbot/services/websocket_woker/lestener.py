from typing import Optional

import websockets
from telebot.async_telebot import AsyncTeleBot
from websockets import WebSocketClientProtocol

from tgbot.services.websocket_woker.reader import DataReader


class WebSocketClient:
    def __init__(self, uri, bot: AsyncTeleBot):
        self.uri = uri
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.bot = bot

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        print("Connected to WebSocket server")

    async def send_data(self, data):
        await self.websocket.send(data)
        print(f"Sent message: {data}")

    async def receive_data(self):
        data = await self.websocket.recv()
        print(f"Received message: {data}")
        return data

    async def run(self):
        await self.connect()

        try:
            while True:
                data = DataReader(await self.receive_data())
                payload = data.get_data()
                print(payload)
                await self.bot.send_message(payload["telegram_id"], payload["message"])
                print(1)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
