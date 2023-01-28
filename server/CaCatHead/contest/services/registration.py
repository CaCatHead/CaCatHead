from django.contrib.auth.models import User

from CaCatHead.contest.models import Team, ContestRegistration, Contest


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
