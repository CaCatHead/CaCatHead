from django.conf import settings
from kombu import Queue, Exchange, serialization

from CaCatHead.config import cacathead_config
from CaCatHead.core.celery.serializers import dumps, loads

broker_url = f'amqp://{settings.RMQ_USER}:{settings.RMQ_PASS}@{settings.RMQ_HOST}:{settings.RMQ_PORT}/'

timezone = settings.TIME_ZONE

task_track_started = True

worker_max_tasks_per_child = cacathead_config.judge.tasks

task_queue_max_priority = 10
task_default_priority = 5

ping_exchange_name = cacathead_config.judge.broadcast.ping
ping_queue_name = f'{ping_exchange_name}.{cacathead_config.judge.name}'

judge_repository_queue_name = cacathead_config.judge.queue.repository
judge_contest_queue_name = cacathead_config.judge.queue.contest
judge_polygon_queue_name = cacathead_config.judge.queue.polygon

task_queues = (
    Queue(ping_queue_name, Exchange(ping_exchange_name, type='fanout', durable=False, delivery_mode=1), durable=False),
    Queue(judge_repository_queue_name),
    Queue(judge_contest_queue_name),
    Queue(judge_polygon_queue_name),
)
task_routes = {
    # Ping 优先级为 10
    'CaCatHead.judge.tasks.ping': {
        'exchange': ping_exchange_name,
        'queue': ping_queue_name,
        'delivery_mode': 'transient'
    },
    # 题库评测优先级为 6, 重测优先级为 7
    'CaCatHead.judge.tasks.judge_repository_submission': {
        'queue': judge_repository_queue_name
    },
    # 比赛评测优先级为 8, 重测优先级为 9
    'CaCatHead.judge.tasks.judge_contest_submission': {
        'queue': judge_contest_queue_name
    },
    # Polygon 评测优先级为 5, 重测优先级为 5
    'CaCatHead.judge.tasks.judge_polygon_submission': {
        'queue': judge_polygon_queue_name
    }
}

# Config custom json serializer
serialization.register('json', dumps, loads,
                       content_type='application/json',
                       content_encoding='utf-8')
accept_content = ['json']
result_serializer = 'json'
task_serializer = 'json'
