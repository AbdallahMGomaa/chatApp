from django.core.management.base import BaseCommand
from kafka.consumers.messaging import MessageConsumer


class Command(BaseCommand):
    help = 'Run the Kafka consumer'

    def handle(self, *args, **options):
        consumer = MessageConsumer()
        consumer.consume_messages()
