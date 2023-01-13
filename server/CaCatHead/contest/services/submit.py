import logging

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import APIException

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.contest.services.registration import make_single_user_team
from CaCatHead.core.constants import Verdict
from CaCatHead.judge.tasks import judge_contest_submission
from CaCatHead.problem.models import Problem
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType

logger = logging.getLogger(__name__)


def user_submit_problem(user: User, contest: Contest, problem: Problem, code: str, language: str):
    registration = ContestRegistration.objects.get_registration(contest, user)

    contest_submission = ContestSubmission(
        repository=contest.problem_repository,
        problem=problem,
        code=code,
        code_length=len(code),
        language=language,
        relative_time=(timezone.now() - contest.start_time).total_seconds()
    )

    registration_id = -1
    if registration is not None and contest.is_running():
        # 比赛提交
        contest_submission.owner = registration.team
        contest_submission.type = ContestSubmissionType.contestant
        contest_submission.save()

        registration_id = registration.id
    elif contest.can_edit_contest(user):
        # 管理员提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.manager
        contest_submission.save()
    elif contest.is_ended():
        # 练习提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.practice
        contest_submission.save()

    try:
        judge_contest_submission.apply_async((contest_submission.id, registration_id), priority=8)
        return contest_submission
    except judge_contest_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise APIException(detail='提交代码失败', code=400)


def rejudge_submission(contest: Contest, contest_submission: ContestSubmission):
    registration_id = -1
    if contest_submission.type == ContestSubmissionType.contestant:
        registration = ContestRegistration.objects.filter(contest=contest, team=contest_submission.owner).first()
        if registration is not None:
            registration_id = registration.id
        else:
            raise APIException(detail='Rejudge 失败，未找到注册信息', code=400)
    else:
        pass

    contest_submission.verdict = Verdict.Waiting
    contest_submission.score = 0
    contest_submission.time_used = 0
    contest_submission.memory_used = 0
    contest_submission.detail = {}
    contest_submission.save()

    try:
        judge_contest_submission.apply_async((contest_submission.id, registration_id), priority=9)
        return contest_submission
    except judge_contest_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise APIException(detail='提交代码失败', code=400)
