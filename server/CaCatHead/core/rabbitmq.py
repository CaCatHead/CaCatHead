import pika
import ujson as json
from django.conf import settings


def send_judge_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT))
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
