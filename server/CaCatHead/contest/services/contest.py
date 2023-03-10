import logging
import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import RestrictedError
from django.utils import timezone
from rest_framework.exceptions import NotFound

from CaCatHead.contest.models import Contest, ContestType, ContestSettings
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.permission.constants import ProblemPermissions, ContestPermissions
from CaCatHead.problem.models import ProblemRepository, Problem, ProblemTypes
from CaCatHead.problem.views import copy_repo_problem
from CaCatHead.problem.views.services import get_main_problem_repo
from CaCatHead.user.services import get_general_user_group

logger = logging.getLogger(__name__)


def make_contest(user: User, title: str, type=ContestType.icpc) -> Contest:
    contest = Contest()
    contest.title = title
    contest.description = title
    contest.type = type
    contest.owner = user
    contest.start_time = timezone.now() + timedelta(days=1)
    contest.end_time = contest.start_time + timedelta(hours=2)
    contest.settings = {ContestSettings.enable_registering: True,
                        ContestSettings.view_standings: True,
                        ContestSettings.view_submissions_after_contest: False,
                        ContestSettings.view_submission_checker_info: False}

    problem_repository = ProblemRepository()
    problem_repository.name = f'{title} 比赛题库'
    problem_repository.is_public = False
    problem_repository.is_contest = True
    problem_repository.owner = user
    problem_repository.save()
    contest.problem_repository = problem_repository

    contest.save()

    # 默认开启注册权限
    Contest.objects.grant_group_permission(get_general_user_group(), ContestPermissions.RegisterContest, contest.id)

    return contest


def edit_contest_payload(user: User, contest: Contest, payload) -> Contest:
    """
    使用传入的 Payload，更新比赛信息
    Payload 见 CaCatHead.contest.serializers.EditContestPayloadSerializer
    """

    def contains(key: str):
        return key in payload and payload[key] is not None

    if contains('title'):
        contest.title = payload['title']
    if contains('type'):
        contest.type = payload['type']
    if contains('description'):
        contest.description = payload['description']
    if contains('start_time'):
        contest.start_time = payload['start_time']
    if contains('end_time'):
        end_time = payload['end_time']
        if end_time > contest.start_time:
            contest.end_time = end_time
    if contains('freeze_time'):
        freeze_time = payload['freeze_time']
        if contest.start_time <= freeze_time <= contest.end_time:
            contest.freeze_time = freeze_time
    if contains('password'):
        contest.password = payload['password']
    if contains('is_public'):
        contest.is_public = payload['is_public']

    # 开关普通用户注册权限
    if contains('enable_registering'):
        # Deprecate: 修复之前错误的状态
        if ContestSettings.enable_registering not in contest.settings:
            contest.settings[ContestSettings.enable_registering] = True

        old_flag = contest.settings[ContestSettings.enable_registering]
        new_flag = payload['enable_registering']
        if old_flag != new_flag:
            if new_flag:
                Contest.objects.grant_group_permission(get_general_user_group(),
                                                       ContestPermissions.RegisterContest,
                                                       contest.id)
            else:
                Contest.objects.revoke_group_permission(get_general_user_group(),
                                                        ContestPermissions.RegisterContest,
                                                        contest.id)
            contest.settings[ContestSettings.enable_registering] = payload['enable_registering']

    if contains('view_standings'):
        contest.settings[ContestSettings.view_standings] = payload['view_standings']
    if contains('view_submissions_after_contest'):
        contest.settings[ContestSettings.view_submissions_after_contest] = payload['view_submissions_after_contest']
    if contains('view_submission_checker_info'):
        contest.settings[ContestSettings.view_submission_checker_info] = payload['view_submission_checker_info']

    if 'problems' in payload and payload['problems'] is not None and isinstance(payload['problems'], list):
        contest = edit_contest_problems(user, contest, payload['problems'])

    contest.save()
    return Contest.objects.filter(id=contest.id).first()


def edit_contest_problems(user: User, contest: Contest, problems: list[str]):
    """
    更新比赛的题目列表:
    user: 操作比赛列表的当前用户
    contest: 比赛
    problems: Polygon Problem ID 列表
    """
    # 准备加入题库的 Polygon Problem 列表
    polygon_problems = []
    # Polygon Problem Info 信息 -> 新的 display_id 映射
    problem_info_display_id = {}
    # 查找对应的 Polygon Problems，检查是否拥有加入题库的权限
    for (display_id, polygon_id) in enumerate(problems):
        problem: Problem = Problem.objects.filter_user_permission(user=user,
                                                                  problemrepository=get_main_problem_repo(),
                                                                  display_id=polygon_id,
                                                                  permission=ProblemPermissions.Copy).first()
        if problem is not None:
            if problem.problem_info_id in problem_info_display_id:
                raise BadRequest(detail=f'你不能重复添加 Polygon 题目 #{polygon_id}.')
            else:
                problem_info_display_id[problem.problem_info_id] = display_id
                polygon_problems.append(problem)
        else:
            raise NotFound(detail=f'未找到 Polygon 题目 #{polygon_id}，或者权限不足')

    # Polygon Problem Info 信息 -> 旧 Contest Problem 映射
    problem_info_contest_problem = {}
    # 复用旧题目时，先将旧题目的 display_id 移动到临时的地方，避免 display_id 冲突
    temp_base_display_id = random.randint(1000000, 1000000000)
    # 尝试删除之前比赛使用的题目
    for old_problem in Problem.objects.filter(repository_id=contest.problem_repository_id).all():
        # 旧的题目已经被加入过了比赛，直接使用旧题目，不删除它
        if old_problem.problem_info_id in problem_info_display_id:
            if old_problem.problem_info_id not in problem_info_contest_problem:
                problem_info_contest_problem[old_problem.problem_info_id] = old_problem
                # 移动旧题目的 display_id 到临时的地方
                old_problem.display_id = temp_base_display_id + old_problem.display_id
                old_problem.save()
            else:
                # 该 Polygon Problem 对应了该 Contest 的很多 Problem，疑似旧的 Problem 未被删除
                raise BadRequest(detail=f'#{old_problem.display_id}. {old_problem.title} 重复存在')
        else:
            # 尝试删除旧题目
            try:
                old_problem.delete()
            except RestrictedError as ex:
                # 有 ContestSubmission 引用这个题目
                logger.error('Delete old contest problem fails: %r', ex)
                raise BadRequest(detail=f'#{old_problem.display_id}. {old_problem.title} 有提交存在，删除失败')

    # 清空旧的题库
    contest.problem_repository.problems.clear()

    # 向题库中添加题目
    for (display_id, polygon_problem) in enumerate(polygon_problems):
        # 推导题目类型，目前只支持 AC 和 Score 两种题目
        problem_type = ProblemTypes.AC
        if contest.type == ContestType.ioi:
            problem_type = ProblemTypes.Score

        if polygon_problem.problem_info_id in problem_info_contest_problem:
            # 复用比赛中的旧题目
            new_problem = problem_info_contest_problem[polygon_problem.problem_info_id]
            new_problem.display_id = display_id
            new_problem.title = polygon_problem.title
            new_problem.problem_type = problem_type  # 支持交互题
            new_problem.time_limit = polygon_problem.time_limit
            new_problem.memory_limit = polygon_problem.memory_limit
            new_problem.save()
            contest.problem_repository.problems.add(new_problem)
        else:
            # 添加新的比赛题目
            copy_repo_problem(user=contest.owner, repo=contest.problem_repository,
                              problem=polygon_problem, display_id=display_id, problem_type=problem_type)

    contest.extra_info['polygon_problems'] = [{'display_id': p.display_id} for p in polygon_problems]

    return contest
