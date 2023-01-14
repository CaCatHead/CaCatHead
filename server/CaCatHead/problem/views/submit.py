import logging

from django.contrib.auth.models import User

from CaCatHead.core.constants import Verdict
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.judge.tasks import judge_polygon_submission, judge_repository_submission
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.submission.models import Submission
from CaCatHead.submission.utils import can_rejudge_submission

logger = logging.getLogger(__name__)


def submit_problem_code(is_repo: bool, user: User, repo: ProblemRepository, problem: Problem, payload: dict):
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

    if is_repo:
        try:
            judge_repository_submission.apply_async((submission.id,), priority=6)
            return submission
        except judge_repository_submission.OperationalError as ex:
            logger.exception('Sending task raised: %r', ex)
            raise BadRequest(detail='提交题库代码失败')
    else:
        try:
            judge_polygon_submission.delay(submission.id)
            return submission
        except judge_polygon_submission.OperationalError as ex:
            logger.exception('Sending task raised: %r', ex)
            raise BadRequest(detail='提交 Polygon 代码失败')


def submit_repository_problem_code(user: User, repo: ProblemRepository, problem: Problem, payload: dict):
    return submit_problem_code(True, user, repo, problem, payload)


def submit_polygon_problem_code(user: User, repo: ProblemRepository, problem: Problem, payload: dict):
    return submit_problem_code(False, user, repo, problem, payload)


def rejudge_problem_code(is_repo: bool, submission: Submission):
    if not can_rejudge_submission(submission):
        raise BadRequest(detail='Rejudge 失败，请勿频繁 Rejudge')

    submission.verdict = Verdict.Waiting
    submission.judged = None
    submission.score = 0
    submission.time_used = 0
    submission.memory_used = 0
    submission.detail = {}
    submission.save()

    if is_repo:
        try:
            judge_repository_submission.apply_async((submission.id,), priority=7)
            return submission
        except judge_repository_submission.OperationalError as ex:
            logger.exception('Sending task raised: %r', ex)
            raise BadRequest(detail='重测题库代码失败')
    else:
        try:
            judge_polygon_submission.delay(submission.id)
            return submission
        except judge_polygon_submission.OperationalError as ex:
            logger.exception('Sending task raised: %r', ex)
            raise BadRequest(detail='重测 Polygon 代码失败')


def rejudge_repository_problem_code(submission: Submission):
    return rejudge_problem_code(True, submission)


def rejudge_polygon_problem_code(submission: Submission):
    return rejudge_problem_code(False, submission)
