from confluent_kafka import Producer
from django.conf import settings

class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': settings.KAFKA_BROKER_URL,
            
        })

    def send_message(self, topic, message):
        self.producer.produce(topic, message.encode('utf-8'))
        self.producer.flush()

    def close(self):
        self.producer.close()
