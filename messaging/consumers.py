import json
from channels.generic.websocket import AsyncWebsocketConsumer

from django.conf import settings
from kafka.producers.producer import KafkaProducer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None
        self.kafka_producer = None

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        self.room_name = self.scope['user'].username
        self.room_group_name = 'chat_%s' % self.room_name
        self.kafka_producer = KafkaProducer()

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
        sender = self.room_name
        receiver_username = data['receiver']
        content = data['content']

        self.kafka_producer.send_message(
            topic=settings.KAFKA_CHAT_TOPIC,
            message=json.dumps({
                "sender": sender,
                "receiver": receiver_username,
                "content": content
            })
        )


        # await self.channel_layer.group_send(
        #     'chat_%s' % receiver_username,
        #     {
        #         'type': 'chat_message',
        #         'message': {'content': content, 'sender': sender}
        #     }
        # )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

