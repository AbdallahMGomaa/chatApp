from kafka.consumers.messaging import MessageConsumer

if __name__ == "__main__":
    message_consumer = MessageConsumer()
    message_consumer.consume_messages()
