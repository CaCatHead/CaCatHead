from django.contrib.auth.models import User

from CaCatHead.core.constants import Verdict
from CaCatHead.core.rabbitmq import send_judge_message
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.submission.models import Submission


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
    message = {
        'submission_id': submission.id,
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
    send_judge_message(message)
    return submission


def rejudge_problem_code(submission: Submission):
    submission.judged = None
    submission.verdict = Verdict.Waiting
    submission.score = 0
    submission.time_used = 0
    submission.memory_used = 0
    submission.detail = {}
    submission.save()

    problem = submission.problem
    message = {
        'submission_id': submission.id,
        'code': submission.code,
        'language': submission.language,
        'problem_id': problem.id,
        'problem_judge_id': problem.problem_info.problem_judge.id,
        'problem_type': problem.problem_type,
        'time_limit': problem.time_limit,
        'memory_limit': problem.memory_limit,
        'testcase_detail': problem.problem_info.problem_judge.testcase_detail,
        'extra_info': problem.problem_info.problem_judge.extra_info
    }
    send_judge_message(message)

    return submission
