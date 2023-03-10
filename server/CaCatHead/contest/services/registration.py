import logging

from django.contrib.auth.models import User

from CaCatHead.contest.models import Team, ContestRegistration, Contest
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.user.services import register_student_user

logger = logging.getLogger(__name__)


def make_single_user_team(user: User) -> Team:
    team = Team.objects.filter(owner=user, single_user=True).first()
    if team is not None:
        return team
    team = Team(
        owner=user,
        name=user.userinfo.nickname,
        single_user=True
    )
    team.save()
    team.members.add(user)
    return team


def single_user_register(user: User, contest: Contest, name: str = None, extra_info: dict = {}) -> ContestRegistration:
    team = make_single_user_team(user)
    registration = ContestRegistration.objects.filter(team=team, contest=contest).first()
    if registration is None:
        registration = ContestRegistration()
    registration.name = name if name is not None else team.name
    registration.team = team
    registration.contest = contest
    registration.extra_info = extra_info
    registration.save()
    return registration


def generate_registrations(contest: Contest, payload):
    registrations = payload['registrations']
    if not isinstance(registrations, list):
        raise BadRequest('输入表格格式非法')

    for p in registrations:
        username = p['username']
        password = p['password']
        nickname = p['team']
        meta = p['meta']

        try:
            user = register_student_user(username, f'{username}@cacathead.cn', password, nickname=nickname)
            single_user_register(user, contest, nickname, meta)
        except Exception as ex:
            logger.error(ex)
            raise BadRequest(f'{nickname} 注册失败')
