import pika
import ssl

from services.rabbit.constants import SupportedQueues
from settings import settings
import json


class RabbitMQBroker:
    def __init__(self):
        ssl_context = ssl.create_default_context()

        self.connection_params = pika.ConnectionParameters(
            host=settings.RMQ_HOST,
            port=settings.RMQ_PORT,
            virtual_host=settings.RMQ_VIRTUAL_HOST,
            credentials=pika.PlainCredentials(username=settings.RMQ_USER, password=settings.RMQ_PASSWORD),
            ssl_options=pika.SSLOptions(context=ssl_context)
        )

    def get_connection(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(parameters=self.connection_params)

    def send_message(self, message: dict, queue_name: str):
        with self.get_connection() as connection:
            with connection.channel() as channel:
                channel.queue_declare(queue=queue_name)

                message_json_str = json.dumps(message)

                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=message_json_str.encode()
                )

    def setup_queues(self, channel: pika.adapters.blocking_connection.BlockingChannel, queues: list[str]):
        for queue in queues:
            channel.queue_declare(queue=queue, durable=True)

    def consume_message(self, channel: pika.adapters.blocking_connection.BlockingChannel):
        queues = SupportedQueues.get_queues()
        self.setup_queues(channel, queues)
        print(5555555555)

        for queue in queues:
            print(queue, 32323233232)
            channel.basic_consume(
                queue=queue,
                on_message_callback=SupportedQueues.get_handler(queue),
            )

        channel.start_consuming()



rabbitmq_broker = RabbitMQBroker()
