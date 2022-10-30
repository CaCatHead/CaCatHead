from django.contrib.auth.models import User
from django.db import models

from CaCatHead.problem.models import Problem, MAIN_PROBLEM_REPOSITORY, ProblemInfo, ProblemContent, ProblemJudge


def make_problem(title: str, user: User, display_id=None):
    print(user)
    print(display_id)

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


def edit_problem(pid: int):
    problem = Problem.objects.get(id=pid)
    return problem
