import logging

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from CaCatHead.config import cacathead_config
from CaCatHead.judge.models import JudgeNode
from CaCatHead.judge.tasks import ping

logger = logging.getLogger(__name__)


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
        ping.apply_async((timezone.now(),), queue='', exchange=cacathead_config.judge.broadcast.ping)
        logger.info('Sending ping judge nodes messages OK ')
