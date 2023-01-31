import logging

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from CaCatHead.config import cacathead_config
from CaCatHead.contest.models import Contest
from CaCatHead.contest.services.submit import rejudge_submission
from CaCatHead.core.constants import Verdict
from CaCatHead.judge.models import JudgeNode
from CaCatHead.judge.tasks import ping
from CaCatHead.submission.models import ContestSubmission

logger = logging.getLogger(__name__)


class RejudgeTestcaseError(CronJobBase):
    code = 'CaCatHead.judge.cron'

    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        subs: list[ContestSubmission] = ContestSubmission.objects.filter(verdict=Verdict.TestCaseError).all()
        for sub in subs:
            try:
                contest = Contest.objects.filter(problem_repository=sub.repository).first()
                if contest is not None:
                    rejudge_submission(contest, sub)
                else:
                    logger.error('Rejudge TestcaseError contest submission fails: can not find contest')
            except Exception as ex:
                logger.exception(ex)
                logger.error('Rejudge TestcaseError contest submission fails')


class PingJudgeNode(CronJobBase):
    code = 'CaCatHead.judge.cron'

    RUN_EVERY_MINS = 1  # every minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        logger.info('Start sending ping judge nodes messages')
        now = timezone.now()
        for node in JudgeNode.objects.filter():
            delta = (now - node.updated).total_seconds()
            if delta >= 60 * 60:
                node.delete()
            elif delta >= 90:
                JudgeNode.objects.filter(id=node.id).update(active=False)
        try:
            ping.apply_async((timezone.now().isoformat(),),
                             queue='', exchange=cacathead_config.judge.broadcast.ping, priority=10)
            logger.info('Sending ping judge nodes messages OK')
        except Exception as ex:
            logger.exception(ex)
            logger.error('Sending ping judge nodes messages Fails')
