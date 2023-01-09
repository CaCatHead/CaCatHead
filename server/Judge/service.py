import logging

import pika
from django.conf import settings
from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from CaCatHead.config import cacathead_config
from Judge.ping import handle_ping
from Judge.submission import SubmissionTask

logger = logging.getLogger('Judge.service')


class JudgeService:
    def __init__(self):
        credentials = pika.PlainCredentials(username=cacathead_config.rabbitmq.username,
                                            password=cacathead_config.rabbitmq.password)
        parameters = pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

        # 判题消息队列
        channel = self.connection.channel()
        queue_name = settings.DEFAULT_JUDGE_QUEUE
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=self.consume)

        # Ping 消息队列
        exchange_name = cacathead_config.judge.ping
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        queue_name = f'{exchange_name}-{cacathead_config.judge.name}'
        channel.queue_declare(queue=queue_name, exclusive=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=self.ping)

        self.channel = channel

    @staticmethod
    def ping(channel: Channel, method: Basic.Deliver, _properties: BasicProperties, _body: bytes):
        logger.info(f'Receive a new ping task from exchange "{method.exchange}"')
        try:
            handle_ping()
        except Exception:
            pass
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f'Handle ping task OK')

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
