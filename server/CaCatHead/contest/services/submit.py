import logging

from django.contrib.auth.models import User
from django.utils import timezone

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.contest.services.registration import make_single_user_team
from CaCatHead.contest.tasks import refresh_standing
from CaCatHead.core.constants import Verdict
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.judge.services.payload import JudgeSubmissionPayload
from CaCatHead.judge.tasks import judge_contest_submission
from CaCatHead.problem.models import Problem
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType
from CaCatHead.submission.utils import can_rejudge_submission

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

    if registration is not None and contest.is_running():
        # 比赛提交
        contest_submission.owner = registration.team
        contest_submission.type = ContestSubmissionType.contestant
        contest_submission.save()
    elif contest.can_edit_contest(user):
        # 管理员提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.manager
        contest_submission.save()

        registration = None
    elif contest.is_ended():
        # 练习提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.practice
        contest_submission.save()

        registration = None

    try:
        payload = JudgeSubmissionPayload.make(contest_submission=contest_submission, registration=registration)
        if registration is not None:
            judge_contest_submission.apply_async((payload,), priority=8,
                                                 link=refresh_standing.signature((registration.id,), priority=1))
        else:
            judge_contest_submission.apply_async((payload,), priority=8)
        return contest_submission
    except judge_contest_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise BadRequest(detail='提交代码失败')


def rejudge_submission(contest: Contest, contest_submission: ContestSubmission):
    registration = None
    if contest_submission.type == ContestSubmissionType.contestant:
        rg = ContestRegistration.objects.filter(contest=contest, team=contest_submission.owner).first()
        if rg is not None:
            registration = rg
        else:
            raise BadRequest(detail='Rejudge 失败，未找到注册信息')
    else:
        pass

    if not can_rejudge_submission(contest_submission):
        raise BadRequest(detail='Rejudge 失败，请勿频繁 Rejudge')

    contest_submission.verdict = Verdict.Waiting
    contest_submission.score = 0
    contest_submission.time_used = 0
    contest_submission.memory_used = 0
    contest_submission.detail = {}
    contest_submission.save()

    try:
        payload = JudgeSubmissionPayload.make(contest_submission=contest_submission, registration=registration)
        if registration is not None:
            judge_contest_submission.apply_async((payload,), priority=9,
                                                 link=refresh_standing.signature((registration.id,), priority=2))
        else:
            judge_contest_submission.apply_async((payload,), priority=9)
        return contest_submission
    except judge_contest_submission.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        raise BadRequest(detail='提交代码失败')
