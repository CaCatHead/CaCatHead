import pika
import ujson as json
from django.conf import settings
from django.contrib.auth.models import User

from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.submission.models import Submission


def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RMQ_HOST, port=settings.RMQ_PORT))
    channel = connection.channel()
    channel.queue_declare(queue='judge_task', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=settings.DEFAULT_JUDGE_QUEUE,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )


def submit_problem_code(user: User, repo: ProblemRepository, problem: Problem, payload: dict):
    code = payload['code']
    language = payload['language']  # TODO: check language here
    submission = Submission(
        repository=repo,
        problem=problem,
        owner=user,
        code=code,
        language=language,
    )
    submission.save()
    message = {
        'submission_id': submission.id,
        'code': code,
        'language': language,
        'problem_id': problem.id,
        'problem_type': problem.problem_type,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'testcase_detail': problem.problem_info.problem_judge.testcase_detail,
        'extra_info': problem.problem_info.problem_judge.extra_info
    }
    send_message(message)
    return submission
