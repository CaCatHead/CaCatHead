from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import NotFound

from CaCatHead.contest.models import Contest, ContestType, ContestSettings
from CaCatHead.permission.constants import ProblemPermissions
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.problem.views import copy_repo_problem, MAIN_PROBLEM_REPOSITORY


def make_contest(user: User, title: str, type=ContestType.icpc) -> Contest:
    contest = Contest()
    contest.title = title
    contest.description = title
    contest.type = type
    contest.owner = user
    contest.start_time = timezone.now() + timedelta(days=1)
    contest.end_time = contest.start_time + timedelta(hours=2)
    contest.settings = {ContestSettings.view_standings: True,
                        ContestSettings.view_submissions_after_contest: False}

    problem_repository = ProblemRepository()
    problem_repository.name = f'{title} 比赛题库'
    problem_repository.is_public = False
    problem_repository.is_contest = True
    problem_repository.owner = user
    problem_repository.save()
    contest.problem_repository = problem_repository

    contest.save()
    return contest


def edit_contest_payload(user: User, contest: Contest, payload) -> Contest:
    # payload see CaCatHead.contest.serializers.EditContestPayloadSerializer
    if 'title' in payload:
        contest.title = payload['title']
    if 'description' in payload and payload['description'] is not None:
        contest.description = payload['description']
    if 'start_time' in payload:
        contest.start_time = payload['start_time']
    if 'end_time' in payload:
        end_time = payload['end_time']
        if end_time > contest.start_time:
            if contest.freeze_time is None or 'freeze_time' in payload or end_time >= contest.freeze_time:
                contest.end_time = end_time
    if 'freeze_time' in payload:
        freeze_time = payload['freeze_time']
        if contest.start_time <= freeze_time <= contest.end_time:
            contest.freeze_time = freeze_time
    if 'password' in payload:
        contest.password = payload['password']
    if 'is_public' in payload:
        contest.is_public = payload['is_public']

    if 'view_standings' in payload:
        contest.settings[ContestSettings.view_standings] = payload['view_standings']
    if 'view_submissions_after_contest' in payload:
        contest.settings[ContestSettings.view_submissions_after_contest] = payload['view_submissions_after_contest']

    if 'problems' in payload and payload['problems'] is not None and isinstance(payload['problems'], list):
        contest = edit_contest_problems(user, contest, payload['problems'])

    contest.save()
    return Contest.objects.filter(id=contest.id).first()


def edit_contest_problems(user: User, contest: Contest, problems: list[str]):
    # 删除之前的题目
    old_problems = map(lambda p: p.id, contest.problem_repository.problems.all())
    contest.problem_repository.problems.clear()
    for pid in old_problems:
        problem = Problem.objects.get(id=pid)
        if problem is not None:
            problem.delete()

    # 复制新的题目
    for p in problems:
        problem = Problem.objects.filter_user_permission(user=user,
                                                         problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                         id=p,
                                                         permission=ProblemPermissions.Copy).first()
        if problem is not None:
            copy_repo_problem(user=contest.owner, repo=contest.problem_repository, problem=problem)
        else:
            raise NotFound(detail=f'未找到题目{p}，或者权限不足')
    return contest
