import json
import ssl

import pika
from settings import settings


class RabbitMQBroker:
    def __init__(self):
        ssl_context = ssl.create_default_context()

        self.connection_params = pika.ConnectionParameters(
            host=settings.RMQ_HOST,
            port=settings.RMQ_PORT,
            virtual_host=settings.RMQ_VIRTUAL_HOST,
            credentials=pika.PlainCredentials(username=settings.RMQ_USER, password=settings.RMQ_PASSWORD),
            ssl_options=pika.SSLOptions(context=ssl_context),
        )

    def get_connection(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(parameters=self.connection_params)

    def send_message(self, message: dict, queue_name: str):
        with self.get_connection() as connection:
            with connection.channel() as channel:
                channel.queue_declare(queue=queue_name, durable=True)

                message_json_str = json.dumps(message)

                channel.basic_publish(exchange="", routing_key=queue_name, body=message_json_str.encode())


rabbitmq_broker = RabbitMQBroker()
