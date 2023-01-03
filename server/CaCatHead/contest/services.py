from datetime import datetime, timedelta

from django.contrib.auth.models import User

from CaCatHead.contest.models import Contest
from CaCatHead.problem.models import ProblemRepository


def make_contest(user: User, title: str, type: str = 'icpc') -> Contest:
    contest = Contest()
    contest.title = title
    contest.type = type
    contest.owner = user
    contest.start_time = datetime.now() + timedelta(days=1)
    contest.end_time = contest.start_time + timedelta(hours=2)

    problem_repository = ProblemRepository()
    problem_repository.name = f'Contest {title}'
    problem_repository.is_public = False
    problem_repository.owner = user
    problem_repository.save()
    contest.problem_repository = problem_repository

    contest.save()
    return contest
