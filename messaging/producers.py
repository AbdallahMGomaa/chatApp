from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self, brokers):
        self.producer = Producer({'bootstrap.servers': brokers})

    def send_message(self, topic, message):
        self.producer.produce(topic, message.encode('utf-8'))
        self.producer.flush()

    def close(self):
        self.producer.close()
