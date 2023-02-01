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


class RejudgeErrorSubmission(CronJobBase):
    """
    每分钟自动重测可能是挂掉的提交，可能是遇到 TestcaseError 或者消息丢失一直 Waiting
    单次最多重测 MAX_REJUDGE_COUNT 次（30 次）
    """

    code = 'CaCatHead.judge.cron.RejudgeErrorSubmission'

    RUN_EVERY_MINS = 1

    MAX_REJUDGE_COUNT = 30

    MAX_WAITING_SEC = 60

    MAX_RUNNING_SEC = 60 * 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        logger.info('Start finding error contest submissions to rejudge')

        rejudge_count = 0

        # 重测 TestcaseError 的提交
        error_subs: list[ContestSubmission] = ContestSubmission.objects.filter(verdict=Verdict.TestCaseError).all()
        for sub in error_subs:
            if rejudge_count == self.MAX_REJUDGE_COUNT:
                break
            try:
                contest = Contest.objects.filter(problem_repository=sub.repository).first()
                if contest is not None:
                    logger.info(f"Rejudge TestcaseError contest submission #{sub.id}.")
                    rejudge_submission(contest, sub)
                    rejudge_count += 1
                else:
                    logger.error('Rejudge TestcaseError contest submission fails: can not find contest')
            except Exception as ex:
                logger.exception(ex)
                logger.error('Rejudge TestcaseError contest submission fails')

        # 重测等待时长超过 1 分钟的提交
        waiting_subs: list[ContestSubmission] = ContestSubmission.objects.filter(verdict=Verdict.Waiting).all()
        for sub in waiting_subs:
            if rejudge_count == self.MAX_REJUDGE_COUNT:
                break
            try:
                contest = Contest.objects.filter(problem_repository=sub.repository).first()
                if contest is not None:
                    delta = (timezone.now() - sub.updated).total_seconds()
                    if delta >= self.MAX_WAITING_SEC:
                        logger.info(f"Rejudge Waiting contest submission #{sub.id}.")
                        rejudge_submission(contest, sub)
                        rejudge_count += 1
                else:
                    logger.error('Rejudge Waiting contest submission fails: can not find contest')
            except Exception as ex:
                logger.exception(ex)
                logger.error('Rejudge Waiting contest submission fails')

        # 重测运行时长超过 10 分钟的提交
        running_subs: list[ContestSubmission] = ContestSubmission.objects.filter(verdict=Verdict.Running).all()
        for sub in running_subs:
            if rejudge_count == self.MAX_REJUDGE_COUNT:
                break
            try:
                contest = Contest.objects.filter(problem_repository=sub.repository).first()
                if contest is not None:
                    delta = (timezone.now() - sub.updated).total_seconds()
                    if delta >= self.MAX_RUNNING_SEC:
                        logger.info(f"Rejudge Running contest submission #{sub.id}.")
                        rejudge_submission(contest, sub)
                        rejudge_count += 1
                else:
                    logger.error('Rejudge Running contest submission fails: can not find contest')
            except Exception as ex:
                logger.exception(ex)
                logger.error('Rejudge Running contest submission fails')

        logger.info(f"Rejudge {rejudge_count} contest submissions")


class PingJudgeNode(CronJobBase):
    code = 'CaCatHead.judge.cron.PingJudgeNode'

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
