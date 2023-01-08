import pika
import ujson as json
from django.conf import settings

from CaCatHead.config import cacathead_config


def send_judge_message(message):
    credentials = pika.PlainCredentials(username=cacathead_config.rabbitmq.username,
                                        password=cacathead_config.rabbitmq.password)
    parameters = pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=settings.DEFAULT_JUDGE_QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=settings.DEFAULT_JUDGE_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
