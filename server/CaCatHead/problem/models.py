from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.models import BaseModel
from CaCatHead.permission.managers import PermissionManager


class ProblemTypes(models.TextChoices):
    # OI 赛制, 计算得分
    Score = 'classic_score'
    # XCPC 赛制, 返回是否正确
    AC = 'classic_ac'
    # 交互题
    Interactive = 'interactive'
    # 自定义判题逻辑
    Custom = 'custom'


class DefaultCheckers(models.TextChoices):
    custom = 'custom'
    fcmp = 'fcmp'
    hcmp = 'hcmp'
    lcmp = 'lcmp'
    ncmp = 'ncmp'
    nyesno = 'nyesno'
    rcmp4 = 'rcmp4'
    rcmp6 = 'rcmp6'
    rcmp9 = 'rcmp9'
    wcmp = 'wcmp'
    yesno = 'yesno'


class SourceCodeTypes(models.TextChoices):
    checker = 'checker'
    generator = 'generator'
    validator = 'validator'
    solution = 'solution'


class ProblemContent(BaseModel):
    title = models.CharField(max_length=512, verbose_name=_(u"标题"))

    description = models.TextField(blank=True, null=True, verbose_name=_(u"题目描述"))

    input = models.TextField(blank=True, null=True, verbose_name=_(u"输入描述"))

    output = models.TextField(blank=True, null=True, verbose_name=_(u"输出描述"))

    sample = models.JSONField(default=list, verbose_name=_(u"样例"))

    hint = models.TextField(blank=True, null=True, verbose_name=_(u"解答提示"))

    source = models.TextField(blank=True, null=True, verbose_name=_(u"题目来源"))

    extra_content = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'problem_content'
        app_label = 'problem'
        verbose_name = _(u"题目内容")
        verbose_name_plural = _(u"题目内容列表")


class SourceCode(BaseModel):
    type = models.CharField(choices=SourceCodeTypes.choices, max_length=32, verbose_name=_(u"代码类型"))

    code = models.TextField(blank=True, max_length=65535, verbose_name=_(u"代码"))

    code_length = models.IntegerField(default=0, verbose_name=_(u"代码长度"))

    language = models.CharField(max_length=32, verbose_name=_(u"程序语言"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'source_code'
        verbose_name = _(u"题目代码")
        verbose_name_plural = _(u"题目代码列表")


class ProblemJudge(models.Model):
    problem_type = models.CharField(default=ProblemTypes.AC,
                                    max_length=32,
                                    choices=ProblemTypes.choices,
                                    verbose_name=_(u"题目类型"))

    time_limit = models.IntegerField(default=1000, verbose_name=_(u"时间限制"))

    memory_limit = models.IntegerField(default=262144, verbose_name=_(u"内存限制"))

    score = models.IntegerField(default=0, verbose_name=_(u"题目总分"))

    testcase_count = models.IntegerField(default=0, verbose_name=_(u"测试用例总数"))

    testcase_version = models.IntegerField(default=0, verbose_name=_(u"测试用例版本"))

    testcase_detail = models.JSONField(default=list, verbose_name=_(u"测试用例配置"))

    checker = models.CharField(default=DefaultCheckers.lcmp, choices=DefaultCheckers.choices, max_length=64,
                               verbose_name=_(u"checker"))

    custom_checker = models.ForeignKey(SourceCode, default=None, null=True,
                                       on_delete=models.CASCADE,
                                       related_name='problem_judge_custom_checker',
                                       verbose_name=_(u"自定义 Checker"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'problem_judge'
        app_label = 'problem'
        verbose_name = _(u"题目评测信息")
        verbose_name_plural = _(u"题目评测信息列表")


class ProblemInfo(models.Model):
    problem_content = models.ForeignKey(ProblemContent,
                                        on_delete=models.CASCADE,
                                        related_name='problem_content',
                                        verbose_name=_(u"题目描述内容"))

    problem_judge = models.ForeignKey(ProblemJudge,
                                      on_delete=models.RESTRICT,
                                      related_name='problem_judge',
                                      verbose_name=_(u"评测信息"))

    owner = models.ForeignKey(User,
                              on_delete=models.RESTRICT,
                              related_name='problem_info_owner',
                              verbose_name=_(u"创建者"))

    def __str__(self):
        return f'ProblemInfo #{self.id}'

    class Meta:
        db_table = 'problem_info'

        verbose_name = _(u"题目信息")

        verbose_name_plural = _(u"题目信息列表")


class Problem(BaseModel):
    """数据库中存储的所有题目
    Attributes:
        repo: 题目的分类(cppbase,cpptest,cppexam,dsbase,dstest,dsexam,algobase,algotest,algoexam,others,ccf)
        label: 题目的题号
        title: 题目的标题
        description: 题目的描述
        inputdescription: 题目的输入描述
        outputdescription: 题目的输出描述
        inputsample: 输入样例
        outputsample: 输出样例
        hint: 提示
        source: 题目来源
        timelimit：时间限制（单个testdata）
        memorylimit：内存限制（单个testdata）
        accept_number:题目通过人数
        submit_number:题目提交次数
        score: 本题目总分数
        testdata_count： testdata总个数
        testdata_score: 当前testdata所对应的分数
        create_user: 创建题目的账户
        is_public: 是否公开
    """
    repository = models.ForeignKey('ProblemRepository',
                                   on_delete=models.CASCADE,
                                   related_name='problem_repository',
                                   verbose_name=_(u"所属题库"))

    display_id = models.IntegerField(default=0, verbose_name=_(u"题目显示编号"))

    title = models.CharField(max_length=512, verbose_name=_(u"标题"))

    problem_type = models.CharField(default=ProblemTypes.AC,
                                    max_length=32,
                                    choices=ProblemTypes.choices,
                                    verbose_name=_(u"题目类型"))

    time_limit = models.IntegerField(default=1000, verbose_name=_(u"时间限制"))

    memory_limit = models.IntegerField(default=262144, verbose_name=_(u"内存限制"))

    problem_info = models.ForeignKey(ProblemInfo,
                                     on_delete=models.RESTRICT,
                                     related_name='problem_info',
                                     verbose_name=_(u"题目信息"))

    extra_info = models.JSONField(default=dict, verbose_name=_(u"其他信息"))

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='problem_owner', verbose_name=_(u"创建者"))

    is_public = models.BooleanField(default=True, verbose_name=_(u"是否公开"),
                                    help_text='该项被选择后，题目将会被所有人看到，如果不选择则题目只能被超级用户和管理员看到.')

    # accepted_number = models.IntegerField(default=0, verbose_name=_(u"通过人数"))
    # submit_number = models.IntegerField(default=0, verbose_name=_(u"提交次数"))
    # level = models.IntegerField(default=3, verbose_name=_(u"题目难度"))

    objects = PermissionManager()

    def __str__(self):
        return f'Problem {self.id}. {self.title}'

    class Meta:
        db_table = 'problem'

        ordering = ('repository', 'display_id')

        unique_together = ('repository', 'display_id')

        indexes = [
            models.Index(fields=['repository'], name='problem__repo_index'),
            models.Index(fields=['repository', 'display_id'], name='problem__repo_display_id_index')
        ]

        verbose_name = _(u"题目信息")

        verbose_name_plural = _(u"题目列表")

    def make_update(self):
        Problem.objects.filter(id=self.id).update(updated=timezone.now())


class ProblemRepository(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u"题目仓库名称"))

    is_public = models.BooleanField(default=False, verbose_name=_(u"是否公开"))

    is_contest = models.BooleanField(default=False, verbose_name=_(u"是否为比赛"))

    problems = models.ManyToManyField(Problem, verbose_name=_(u"题目列表"))

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='repo_owner', verbose_name=_(u"创建者"))

    objects = PermissionManager()

    def __str__(self):
        if self.name.endswith('题库'):
            return self.name
        else:
            return f'{self.name}题库'

    class Meta:
        db_table = 'problem_repository'

        verbose_name = _(u"题目仓库")

        verbose_name_plural = _(u"题目仓库列表")

        permissions = (('polygon', 'Can use Polygon'),)
