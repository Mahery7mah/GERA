import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.evenement_id = self.scope['url_route']['kwargs']['evenement_id']
        self.group_name = f'notification_{self.evenement_id}'

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
        pass

    async def send_progress(self, event):
        progress = event['progress']
        await self.send(text_data=json.dumps({
            'progress': progress
        }))