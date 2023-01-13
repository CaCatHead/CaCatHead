import logging

from django.contrib.auth.models import User
from rest_framework.exceptions import APIException

from CaCatHead.core.constants import Verdict
from CaCatHead.judge.tasks import judge_polygon_submission
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.submission.models import Submission

logger = logging.getLogger(__name__)


def submit_problem_code(user: User, repo: ProblemRepository, problem: Problem, payload: dict):
    code = payload['code']
    language = payload['language']
    submission = Submission(
        repository=repo,
        problem=problem,
        owner=user,
        code=code,
        code_length=len(code),
        language=language,
    )
    submission.save()

    try:
        judge_polygon_submission.delay(submission.id)
        return submission
    except judge_polygon_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise APIException(detail='提交代码失败', code=400)


def rejudge_problem_code(submission: Submission):
    submission.judged = None
    submission.verdict = Verdict.Waiting
    submission.score = 0
    submission.time_used = 0
    submission.memory_used = 0
    submission.detail = {}
    submission.save()

    try:
        judge_polygon_submission.delay(submission.id)
        return submission
    except judge_polygon_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise APIException(detail='重测代码失败', code=400)
