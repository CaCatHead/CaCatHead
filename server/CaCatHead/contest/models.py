from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.models import BaseModel
from CaCatHead.permission.constants import ContestPermissions
from CaCatHead.permission.managers import PermissionManager
from CaCatHead.problem.models import ProblemRepository


class ContestType(models.TextChoices):
    icpc = 'icpc'
    ioi = 'ioi'


class ContestSettings(models.TextChoices):
    view_standings = 'view_standings'
    view_submission_checker_info = 'view_submission_checker_info'
    view_submissions_after_contest = 'view_submissions_after_contest'


class Contest(BaseModel):
    title = models.CharField(max_length=256, verbose_name=_(u"标题"))

    type = models.CharField(default=ContestType.icpc, choices=ContestType.choices, max_length=64,
                            verbose_name=_(u"比赛类型"))

    description = models.TextField(default=str, blank=True, verbose_name=_(u"比赛描述信息"))

    start_time = models.DateTimeField(verbose_name=_(u"开始时间"))

    freeze_time = models.DateTimeField(default=None, null=True, verbose_name=_(u"封榜时间"))

    end_time = models.DateTimeField(verbose_name=_(u"结束时间"))

    problem_repository = models.ForeignKey(ProblemRepository, on_delete=models.RESTRICT, verbose_name=_(u"比赛题库"))

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='contest_owner', verbose_name=_(u"创建者"))

    is_public = models.BooleanField(default=False, verbose_name=_(u"是否公开"))

    password = models.CharField(default=None, null=True, blank=True, max_length=256, verbose_name=_(u"注册密码"))

    settings = models.JSONField(default=dict, verbose_name=_(u"比赛设置"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    objects = PermissionManager()

    class Meta:
        db_table = 'contest'

        ordering = ('-start_time',)

        verbose_name = _("比赛")

        verbose_name_plural = _("比赛列表")

    def __str__(self):
        return f'比赛 #{self.id}. {self.title}'

    def is_running(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def is_started(self):
        now = timezone.now()
        return self.start_time <= now

    def is_ended(self):
        now = timezone.now()
        return self.end_time < now

    def enable_settings(self, perm: str) -> bool:
        if perm in self.settings:
            return bool(self.settings[perm])
        else:
            return False

    def has_admin_permission(self, user: User):
        if user.is_superuser or user.is_staff:
            return True
        return Contest.objects.filter_user_permission(user=user, permission=ContestPermissions.EditContest).filter(
            id=self.id).count() > 0

    def can_edit_contest(self, user: User):
        return Contest.objects.filter_user_permission(user=user, permission=ContestPermissions.EditContest).filter(
            id=self.id).count() > 0

    def get_problem(self, display_id: int):
        return self.problem_repository.problems.filter(display_id=display_id).first()


class Team(models.Model):
    name = models.CharField(max_length=256, verbose_name=_(u"名称"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(u"队长"))

    single_user = models.BooleanField(default=False, verbose_name=_(u"用户自己的队伍"))

    members = models.ManyToManyField(User, related_name='members', verbose_name=_(u"队员"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"创建时间"))

    rating = models.IntegerField(default=1500, verbose_name=_("Rating"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'team'

        verbose_name = _("队伍")

        verbose_name_plural = _("队伍列表")


class ContestRegistrationManager(models.Manager):
    def filter_registration(self, contest: Contest):
        return self.filter(contest=contest)

    def filter_register_team(self, contest: Contest):
        return Team.objects.filter(id__in=self.filter(contest=contest).values('team'))

    def filter_register_user(self, contest: Contest):
        members = Team.members.through.objects.filter(
            team_id__in=self.filter_register_team(contest).values('id')).values('user_id')
        return User.objects.filter(id__in=members)

    def get_registration(self, contest: Contest, user: User):
        teams = Team.members.through.objects.filter(user_id=user.id).values('team_id')
        return self.filter(contest=contest, team__in=teams).first()


class ContestRegistration(models.Model):
    name = models.CharField(max_length=256, verbose_name=_(u"名称"))

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name=_(u"所属比赛"))

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_(u"注册队伍"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"创建时间"))

    score = models.IntegerField(default=0, verbose_name=_(u"得分"))

    dirty = models.IntegerField(default=0, verbose_name=_(u"罚时"))

    # 标记是否真正参加了比赛，且提交过代码
    is_participate = models.BooleanField(default=False, verbose_name=_(u"是否参加比赛"))

    standings = models.JSONField(default=dict, verbose_name=_(u"排名信息"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    objects = ContestRegistrationManager()

    class Meta:
        db_table = 'contest_registration'

        ordering = ('-score', 'dirty', '-is_participate')

        indexes = [
            models.Index(fields=['contest', 'team'], name='contest_team_index')
        ]

        verbose_name = _("比赛注册信息")

        verbose_name_plural = _("比赛注册信息列表")


class RatingLog(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name=_(u"比赛"))

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_(u"队伍"))

    rating = models.IntegerField(verbose_name=_(u"原 Rating"))

    delta = models.IntegerField(verbose_name=_(u"Rating 变化量"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"创建时间"))

    class Meta:
        db_table = 'rating_log'

        ordering = ('-created', 'contest', '-rating')

        indexes = [
            models.Index(fields=['contest'], name='rating_log_contest_index')
        ]

        verbose_name = _("Rating 日志")

        verbose_name_plural = _("Rating 日志列表")
