from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from CaCatHead.contest.models import Team
from CaCatHead.core.constants import Verdict
from CaCatHead.problem.models import ProblemRepository, Problem


class Submission(models.Model):
    """提交状态表
    Attributes:
        contest_id: 考试编号,为 0 时表示为练习提交
        label: 题号
        user: 提交的用户名
        code: 提交的代码
        compiler: 语言
        compilerOutput: 编译的输出，一般用户编译失败信息的存储
        status: 当前状态，'正在判题','编译错误','答案错误','答案正确'-->等 (仅有总得分为满分的时候才显示Accept'答案正确')
        length: 代码长度
        submittime: 提交时间
        score: 总得分
        testdata_score: 提交状态生成时，题目的测试用例分值情况。
        detail: 每个样例得了多少分
    """
    repository = models.ForeignKey(ProblemRepository,
                                   on_delete=models.RESTRICT,
                                   related_name='submission_repository',
                                   verbose_name=_(u"所属题库"))

    problem = models.ForeignKey(Problem,
                                on_delete=models.RESTRICT,
                                related_name='submission_problem',
                                verbose_name=_(u"所属题目"))

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='submission_user',
                              verbose_name=_(u"创建者"))

    code = models.TextField(blank=True, max_length=65535, verbose_name=_(u"代码"))

    code_length = models.IntegerField(default=0, verbose_name=_(u"代码长度"))

    language = models.CharField(max_length=32, verbose_name=_(u"程序语言"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"提交时间"))

    judged = models.DateTimeField(blank=True, null=True, verbose_name=_(u"评测时间"))

    verdict = models.CharField(default=Verdict.Waiting, max_length=32, verbose_name=_(u"提交状态和判题结果"))

    score = models.IntegerField(default=0, verbose_name=_(u"总分"))

    time_used = models.IntegerField(default=0, verbose_name=_(u"消耗时间"))

    memory_used = models.IntegerField(default=0, verbose_name=_(u"消耗内存"))

    # 编译错误信息, 每个测试点的用时得分等
    detail = models.JSONField(default=dict, blank=True, verbose_name=_(u"返回详情"))

    class Meta:
        db_table = 'submission'

        ordering = ('-created', '-score')

        verbose_name = _(u"提交信息")

        verbose_name_plural = _(u"提交信息列表")

        indexes = [
            models.Index(fields=['repository'], name='sub__repo_index'),
            models.Index(fields=['repository', 'owner'], name='sub__repo_owner_index'),
        ]


class ContestSubmissionType(models.TextChoices):
    contestant = 'contestant'
    practice = 'practice'
    virtual = 'virtual'
    manager = 'manager'
    out_of_contest = 'out_of_contest'


class ContestSubmission(models.Model):
    repository = models.ForeignKey(ProblemRepository,
                                   on_delete=models.RESTRICT,
                                   related_name='contest_submission_repository',
                                   verbose_name=_(u"所属题库"))

    problem = models.ForeignKey(Problem,
                                on_delete=models.RESTRICT,
                                related_name='contest_submission_problem',
                                verbose_name=_(u"所属题目"))

    owner = models.ForeignKey(Team,
                              on_delete=models.CASCADE,
                              related_name='contest_submission_team',
                              verbose_name=_(u"创建队伍"))

    type = models.CharField(max_length=16, choices=ContestSubmissionType.choices, verbose_name=_(u"比赛提交类型"))

    code = models.TextField(blank=True, max_length=65535, verbose_name=_(u"代码"))

    code_length = models.IntegerField(default=0, verbose_name=_(u"代码长度"))

    language = models.CharField(max_length=32, verbose_name=_(u"程序语言"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"提交时间"))

    # 提交时间相对于比赛开始时间，单位：秒
    relative_time = models.IntegerField(verbose_name=_(u"提交相对时间"))

    judged = models.DateTimeField(blank=True, null=True, verbose_name=_(u"评测时间"))

    verdict = models.CharField(default=Verdict.Waiting, max_length=32, verbose_name=_(u"提交状态和判题结果"))

    score = models.IntegerField(default=0, verbose_name=_(u"总分"))

    time_used = models.IntegerField(default=0, verbose_name=_(u"消耗时间"))

    memory_used = models.IntegerField(default=0, verbose_name=_(u"消耗内存"))

    # 编译错误信息, 每个测试点的用时得分等
    detail = models.JSONField(default=dict, blank=True, verbose_name=_(u"返回详情"))

    class Meta:
        db_table = 'contest_submission'

        ordering = ('-created', '-relative_time', '-score')

        verbose_name = _(u"比赛提交信息")

        verbose_name_plural = _(u"比赛提交信息列表")

        indexes = [
            models.Index(fields=['repository'], name='contest_sub__repo_index'),
            models.Index(fields=['repository', 'owner'], name='contest_sub__repo_owner_index'),
        ]

    def has_user(self, user: User):
        members = self.owner.members.all()
        for member in members:
            if member.id == user.id:
                return True
        return False
