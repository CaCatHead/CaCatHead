import logging

import pika
from django.conf import settings
from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from Judge.submission import SubmissionTask

logger = logging.getLogger('Judge.service')


class JudgeService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT))
        self.channel = self.connection.channel()
        queue_name = settings.DEFAULT_JUDGE_QUEUE
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.consume)

    @staticmethod
    def consume(channel: Channel, method: Basic.Deliver, _properties: BasicProperties, body: bytes):
        logger.info(f'Receive a new judge task from queue "{method.routing_key}"')
        task = SubmissionTask(body)
        task.run()
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        logger.info(f'Start CaCatHead judge service at amqp://{settings.RMQ_HOST}:{settings.RMQ_PORT}')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            logger.info(f'Stop CaCatHead judge service')
        finally:
            self.connection.close()
