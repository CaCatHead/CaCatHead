from CaCatHead.contest.models import Contest, RatingLog


def clear_contest_rating(contest: Contest):
    RatingLog.objects.filter(contest=contest).delete()


def refresh_contest_rating(contest: Contest):
    pass
