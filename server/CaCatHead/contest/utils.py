from enum import Enum

from django.contrib.auth.models import User

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.core.celery.config import timezone


class ContestRole(Enum):
    Admin = 'contest_role.admin'
    Participant = 'contest_role.participant'
    Visitor = 'contest_role.visitor'


class ContestPhase(Enum):
    Before = 'contest_phase.before'
    Coding = 'contest_phase.coding'
    Finished = 'contest_phase.finished'


class ContestStandingsPhase(Enum):
    Before = 'contest_standings_phase.before'
    Running = 'contest_standings_phase.running'
    Frozen = 'contest_standings_phase.frozen'
    Finished = 'contest_standings_phase.finished'


def contest_role(contest: Contest, user: User) -> ContestRole:
    if contest.has_admin_permission(user):
        return ContestRole.Admin
    elif ContestRegistration.objects.get_registration(contest, user) is not None:
        return ContestRole.Participant
    else:
        return ContestRole.Visitor


def contest_phase(contest: Contest) -> ContestPhase:
    now = timezone.now()
    if now < contest.start_time:
        return ContestPhase.Before
    elif now <= contest.end_time:
        return ContestPhase.Coding
    else:
        return ContestPhase.Finished


def contest_standings_phase(contest: Contest) -> ContestStandingsPhase:
    now = timezone.now()
    if now < contest.start_time:
        return ContestStandingsPhase.Before
    elif now <= contest.end_time:
        if contest.freeze_time is not None:
            if now <= contest.freeze_time:
                return ContestStandingsPhase.Running
            else:
                return ContestStandingsPhase.Frozen
        else:
            return ContestStandingsPhase.Running
    else:
        return ContestStandingsPhase.Finished
