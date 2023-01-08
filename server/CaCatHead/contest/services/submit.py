from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import APIException

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.contest.services.registration import make_single_user_team
from CaCatHead.core.constants import Verdict
from CaCatHead.core.rabbitmq import send_judge_message
from CaCatHead.problem.models import Problem
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType


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
    message = {
        'code': code,
        'language': language,
        'problem_id': problem.id,
        'problem_judge_id': problem.problem_info.problem_judge.id,
        'problem_type': problem.problem_type,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'testcase_detail': problem.problem_info.problem_judge.testcase_detail,
        'extra_info': problem.problem_info.problem_judge.extra_info
    }

    if registration is not None and contest.is_running():
        # 比赛提交
        contest_submission.owner = registration.team
        contest_submission.type = ContestSubmissionType.contestant
        contest_submission.save()

        message['contest_submission_id'] = contest_submission.id
        message['registration_id'] = registration.id
    elif contest.can_edit_contest(user):
        # 管理员提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.manager
        contest_submission.save()

        message['contest_submission_id'] = contest_submission.id
    elif contest.is_ended():
        # 练习提交
        contest_submission.owner = make_single_user_team(user)
        contest_submission.type = ContestSubmissionType.practice
        contest_submission.save()

        message['contest_submission_id'] = contest_submission.id

    send_judge_message(message)
    return contest_submission


def rejudge_submission(contest: Contest, contest_submission: ContestSubmission):
    problem = contest_submission.problem
    message = {
        'code': contest_submission.code,
        'language': contest_submission.language,
        'problem_id': problem.id,
        'problem_judge_id': problem.problem_info.problem_judge.id,
        'problem_type': problem.problem_type,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'testcase_detail': problem.problem_info.problem_judge.testcase_detail,
        'extra_info': problem.problem_info.problem_judge.extra_info
    }
    if contest_submission.type == ContestSubmissionType.contestant:
        registration = ContestRegistration.objects.filter(contest=contest, team=contest_submission.owner).first()
        if registration is not None:
            message['registration_id'] = registration.id
            message['contest_submission_id'] = contest_submission.id
        else:
            raise APIException(detail='Rejudge 失败，未找到注册信息', code=400)
    else:
        message['contest_submission_id'] = contest_submission.id

    contest_submission.verdict = Verdict.Waiting
    contest_submission.score = 0
    contest_submission.time_used = 0
    contest_submission.memory_used = 0
    contest_submission.detail = {}
    contest_submission.save()

    send_judge_message(message)
    return contest_submission
