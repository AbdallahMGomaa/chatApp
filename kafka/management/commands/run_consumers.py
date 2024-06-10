from django.core.management.base import BaseCommand
from kafka.consumers.messaging import MessageConsumer


class Command(BaseCommand):
    help = 'Consume chat messages'

    def handle(self, *args, **options):
        consumer = MessageConsumer()
        consumer.consume_messages()
        consumer.close()
