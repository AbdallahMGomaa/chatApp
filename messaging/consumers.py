import json
from channels.generic.websocket import AsyncWebsocketConsumer

from auth_app.models import Account
from messaging.models import Message
from messaging.producers import KafkaProducer
from messaging.serializers import MessageSerializer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        self.room_name = self.scope['user'].username
        self.room_group_name = 'chat_%s' % self.room_name
        self.kafka_producer = KafkaProducer(brokers='kafka:9092')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        self.kafka_producer.close()

    async def receive(self, text_data=None, byte_data=None):
        data = json.loads(text_data)
        receiver_username = data['receiver']
        content = data['content']

        self.kafka_producer.send_message(topic='chat', message=content)

        receiver = await database_sync_to_async(Account.objects.get)(username=receiver_username)
        message = await self.save_message(self.scope['user'], receiver, content)

        await self.channel_layer.group_send(
            'chat_%s' % receiver.username,
            {
                'type': 'chat_message',
                'message': MessageSerializer(message).data
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
