from django.utils import timezone
from django_cron import CronJobBase, Schedule

from CaCatHead.core.rabbitmq import send_ping_message
from CaCatHead.judge.models import JudgeNode


class PingJudgeNode(CronJobBase):
    code = 'CaCatHead.judge.cron'

    RUN_EVERY_MINS = 1  # every minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        print('Ping judge nodes...')
        now = timezone.now()
        for node in JudgeNode.objects.all():
            delta = (now - node.updated).total_seconds()
            if delta >= 60 * 60:
                node.delete()
            elif delta >= 90:
                node.active = False
                node.save()
        send_ping_message({})
