import pika
import ujson as json
from django.conf import settings

from CaCatHead.config import cacathead_config


def get_connection():
    credentials = pika.PlainCredentials(username=cacathead_config.rabbitmq.username,
                                        password=cacathead_config.rabbitmq.password)
    parameters = pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    return connection


def send_ping_message(message):
    connection = get_connection()
    channel = connection.channel()
    exchange_name = cacathead_config.judge.ping
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    channel.basic_publish(exchange=exchange_name, routing_key='', body=json.dumps(message))


def send_judge_message(message):
    connection = get_connection()
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
