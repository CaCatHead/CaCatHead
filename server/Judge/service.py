import pika
from django.conf import settings


class JudgeService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT))
        self.channel = self.connection.channel()

        # judge_task_queue
        self.channel.queue_declare(queue="judge_task", durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.consume)

    def consume(self, ch, method, properties, body):
        # logging.info("GOT A TASK!")
        # task = JudgeTask(body, self.save_result)
        # task.go()
        print('Consume a message')
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Hello, this is judge service')
        self.channel.start_consuming()
