import math

from django.db.models import Sum

from CaCatHead.contest.models import Contest, RatingLog, ContestRegistration, Team
from CaCatHead.user.models import UserInfo

RATING_BASE = 1500


def get_contest_rating_logs(contest: Contest):
    return RatingLog.objects.filter(contest=contest).all()


def clear_contest_rating(contest: Contest):
    RatingLog.objects.filter(contest=contest).delete()
    registrations = ContestRegistration.objects.filter(contest=contest).all()
    for reg in registrations:
        team = reg.team
        new_rating = RatingLog.objects.filter(team=team).aggregate(Sum('delta'))['delta__sum']
        if new_rating is None:
            team.rating = RATING_BASE
            team.save()
            if team.single_user:
                UserInfo.objects.filter(user=team.owner).update(rating=None)
        else:
            team.rating = RATING_BASE + new_rating
            team.save()
            if team.single_user:
                UserInfo.objects.filter(user=team.owner).update(rating=new_rating + RATING_BASE)
    return registrations


class RatingUser(object):
    def __init__(self, rank, old_rating, team=None):
        self.rank = float(rank)
        self.old_rating = int(old_rating)
        self.new_rating = int(old_rating)
        self.seed = 1.0
        self.handle = team
        self.delta = 0


class RatingCalculator(object):

    def __init__(self, registrations: list[ContestRegistration]):
        self.user_list = []
        for (index, registration) in enumerate(registrations):
            if not registration.is_participate:
                continue
            old_rating = registration.team.rating
            user = RatingUser(index + 1, old_rating, registration.team)
            self.user_list.append(user)

    def cal_p(self, user_a, user_b):
        return 1.0 / (1.0 + pow(10, (user_b.old_rating - user_a.old_rating) / 400.0))

    def get_ex_seed(self, user_list, rating, own_user):
        ex_user = RatingUser(0.0, rating)
        result = 1.0
        for user in user_list:
            if user != own_user:
                result += self.cal_p(user, ex_user)
        return result

    def cal_rating(self, user_list, rank, user):
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self.get_ex_seed(user_list, mid, user) < rank:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        # Calculate seed
        for i in range(len(self.user_list)):
            self.user_list[i].seed = 1.0
            for j in range(len(self.user_list)):
                if i != j:
                    self.user_list[i].seed += self.cal_p(self.user_list[j], self.user_list[i])
        # Calculate initial delta and sum_delta
        sum_delta = 0
        for user in self.user_list:
            user.delta = int(
                (self.cal_rating(self.user_list, math.sqrt(user.rank * user.seed), user) - user.old_rating) / 2)
            sum_delta += user.delta
        # Calculate first inc
        inc = int(-sum_delta / len(self.user_list)) - 1
        for user in self.user_list:
            user.delta += inc
        # Calculate second inc
        self.user_list = sorted(self.user_list, key=lambda x: x.old_rating, reverse=True)
        s = min(len(self.user_list), int(4 * round(math.sqrt(len(self.user_list)))))
        sum_s = 0
        for i in range(s):
            sum_s += self.user_list[i].delta
        inc = min(max(int(-sum_s / s), -10), 0)
        # Calculate new rating
        for user in self.user_list:
            user.delta += inc
            user.new_rating = user.old_rating + user.delta
        self.user_list = sorted(self.user_list, key=lambda x: x.rank, reverse=False)


def refresh_contest_rating(contest: Contest):
    registrations = clear_contest_rating(contest)
    calc = RatingCalculator(registrations)
    calc.calculate()
    for user in calc.user_list:
        if user.handle is None:
            continue

        team = user.handle
        log = RatingLog(contest=contest, team=team, rating=user.old_rating, delta=user.delta)
        log.save()
        Team.objects.filter(id=team.id).update(rating=user.new_rating)
        if team.single_user:
            UserInfo.objects.filter(user=team.owner).update(rating=user.new_rating)
