import logging
from datetime import timedelta

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.contest.services.standings import refresh_registration_standing

logger = logging.getLogger(__name__)


class RefreshContestStandings(CronJobBase):
    """
    每 2 分钟自动刷新榜单
    """

    code = 'CaCatHead.contest.cron.RefreshContestStandings'

    RUN_EVERY_MINS = 2

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        start_time = timezone.now()
        end_time = start_time - timedelta(minutes=10)
        contests = Contest.objects.filter(start_time__lt=start_time, end_time__gt=end_time)[:3]
        refreshed = 0

        for contest in contests:
            logger.info(f'Start refresh the standings of contest {contest.title}')
            cnt = 0
            regs = ContestRegistration.objects.filter(contest_id=contest).all()
            for registration in regs:
                try:
                    refresh_registration_standing(registration=registration)
                    cnt += 1
                except Exception as ex:
                    logger.error(ex)
            logger.info(f'Refresh {cnt} standings of contest {contest.title}')
            refreshed += 1

        logger.info(f'Refreshed standings of {refreshed} contests')
