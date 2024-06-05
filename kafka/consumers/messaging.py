import json
import ast
import os
import django
from confluent_kafka import Consumer, KafkaException, KafkaError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatApp.settings')
django.setup()

from django.conf import settings
from messaging.models import Message
from auth_app.models import Account
from messaging.serializers import MessageSerializer


class MessageConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BROKER_URL,
            'group.id': 'chat-group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([settings.KAFKA_CHAT_TOPIC])
        self.channel_layer = get_channel_layer()

    def create_message(self, sender_username, receiver_username, content):
        sender = Account.objects.get(username=sender_username)
        receiver = Account.objects.get(username=receiver_username)

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )
        return message

    def consume_messages(self):
        print('messaging consumer is up')
        try:
            while True:

                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                else:
                    data = ast.literal_eval(msg.value().decode('utf-8'))
                    sender = data['sender']
                    receiver = data['receiver']
                    content = data['content']
                    message = self.create_message(sender, receiver, content)

                    room_group_name = 'chat_%s' % receiver
                    async_to_sync(self.channel_layer.group_send)(
                        room_group_name,
                        {
                            'type': 'chat_message',
                            'message': MessageSerializer(message).data
                        }
                    )
        except Exception as e:
            pass
        finally:
            self.consumer.close()
            print('messaging consumer is down')


