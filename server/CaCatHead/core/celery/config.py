from django.conf import settings
from kombu import Queue, Exchange

from CaCatHead.config import cacathead_config

broker_url = f'amqp://{settings.RMQ_USER}:{settings.RMQ_PASS}@{settings.RMQ_HOST}:{settings.RMQ_PORT}/'

timezone = settings.TIME_ZONE

task_track_started = True

worker_max_tasks_per_child = 1

ping_exchange_name = cacathead_config.judge.broadcast.ping
ping_queue_name = f'{ping_exchange_name}.{cacathead_config.judge.name}'

judge_repository_queue_name = cacathead_config.judge.queue.repository
judge_contest_queue_name = cacathead_config.judge.queue.contest
judge_polygon_queue_name = cacathead_config.judge.queue.polygon

task_queues = (
    Queue(ping_queue_name, Exchange(ping_exchange_name, type='fanout')),
    Queue(judge_repository_queue_name),
    Queue(judge_contest_queue_name),
    Queue(judge_polygon_queue_name),
)
task_routes = {
    'CaCatHead.judge.tasks.ping': {
        'exchange': ping_exchange_name,
        'queue': ping_queue_name,
    },
    'CaCatHead.judge.tasks.judge_repository_submission': {
        'queue': judge_repository_queue_name
    },
    'CaCatHead.judge.tasks.judge_contest_submission': {
        'queue': judge_contest_queue_name
    },
    'CaCatHead.judge.tasks.judge_polygon_submission': {
        'queue': judge_polygon_queue_name
    }
}
