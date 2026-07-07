from channels.generic.websocket import AsyncWebsocketConsumer
import json

class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Optional logic to handle incoming messages from the client
        pass

    # Method to send notification updates
    async def send_notification_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))