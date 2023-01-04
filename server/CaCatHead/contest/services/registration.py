from django.contrib.auth.models import User

from CaCatHead.contest.models import Team


def make_single_user_team(user: User) -> Team:
    team = Team.objects.filter(owner=user).first()
    if team is not None:
        return team
    team = Team()
    team.owner = user
    team.name = user.userinfo.nickname
    team.save()
    team.members.add(user)
    return team
