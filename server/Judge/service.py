import pika
from django.conf import settings


class JudgeService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT))
        self.channel = self.connection.channel()

        queue_name = "judge_task"
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.consume)

    def consume(self, ch, method, properties, body):
        print('Consume a message')
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Hello, this is judge service')
        self.channel.start_consuming()
