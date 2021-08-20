from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # connect to Websocket
    async def connect(self):
        await self.accept()