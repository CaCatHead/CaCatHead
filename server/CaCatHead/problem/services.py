from django.contrib.auth.models import User
from django.db import models

from CaCatHead.problem.models import Problem, MAIN_PROBLEM_REPOSITORY, ProblemInfo, ProblemContent, ProblemJudge


def make_problem(title: str, user: User, display_id=None):
    # init problem content
    problem_content = ProblemContent(title=title)
    problem_content.save()

    # init problem judge info
    problem_judge = ProblemJudge()
    problem_judge.save()

    # init problem info
    problem_info = ProblemInfo(problem_content=problem_content, problem_judge=problem_judge)
    problem_info.save()

    if display_id is None:
        display_id = MAIN_PROBLEM_REPOSITORY.problems.aggregate(models.Max('display_id'))['display_id__max']
        if display_id is None:
            display_id = 0
        else:
            display_id += 1

    problem = Problem(display_id=display_id,
                      title=title,
                      problem_info=problem_info,
                      owner=user,
                      is_public=False)
    problem.save()
    MAIN_PROBLEM_REPOSITORY.problems.add(problem)
    return problem


def edit_problem(problem: Problem, payload: dict):
    if 'title' in payload:
        problem.title = payload['title']
        problem.problem_info.problem_content.title = payload['title']
    if 'display_id' in payload:
        # TODO: check unique display_id
        problem.display_id = payload['display_id']
    if 'time_limit' in payload:
        problem.time_limit = payload['time_limit']
        problem.problem_info.problem_judge.time_limit = payload['time_limit']
    if 'memory_limit' in payload:
        problem.time_limit = payload['memory_limit']
        problem.problem_info.problem_judge.memory_limit = payload['memory_limit']
    if 'description' in payload:
        problem.problem_info.problem_content.description = payload['description']
    if 'input' in payload:
        problem.problem_info.problem_content.input = payload['input']
    if 'output' in payload:
        problem.problem_info.problem_content.output = payload['output']
    if 'sample' in payload:
        problem.problem_info.problem_content.sample = payload['sample']
    if 'hint' in payload:
        problem.problem_info.problem_content.hint = payload['hint']
    if 'source' in payload:
        problem.problem_info.problem_content.source = payload['source']
    if 'extra_content' in payload:
        problem.problem_info.problem_content.extra_content = payload['extra_content']

    problem.save()
    problem.problem_info.problem_content.save()
    problem.problem_info.problem_judge.save()

    return problem
