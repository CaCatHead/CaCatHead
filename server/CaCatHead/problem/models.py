from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY as MAIN_PROBLEM_REPOSITORY_NAME
from CaCatHead.core.models import BaseModel
from CaCatHead.permission.manager import PermissionManager

PROBLEM_TYPES = {
    'classic': 'classic',
    'interactive': 'interactive'
}


class ProblemContent(BaseModel):
    title = models.CharField(max_length=512, verbose_name=_(u"标题"))

    description = models.TextField(blank=True, null=True, verbose_name=_(u"题目描述"))

    input = models.TextField(blank=True, null=True, verbose_name=_(u"输入描述"))

    output = models.TextField(blank=True, null=True, verbose_name=_(u"输出描述"))

    sample = models.TextField(blank=True, null=True, verbose_name=_(u"样例"))

    hint = models.TextField(blank=True, null=True, verbose_name=_(u"解答提示"))

    source = models.TextField(blank=True, null=True, verbose_name=_(u"题目来源"))

    extra_content = models.JSONField(blank=True, null=True, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'problem_content'
        app_label = 'problem'
        verbose_name = _(u"题目内容")
        verbose_name_plural = _(u"题目内容列表")


class ProblemJudge(models.Model):
    problem_type = models.CharField(max_length=32, choices=PROBLEM_TYPES.items(), verbose_name=_(u"题目类型"))

    time_limit = models.IntegerField(default=1000, verbose_name=_(u"时间限制"))

    memory_limit = models.IntegerField(default=262144, verbose_name=_(u"内存限制"))

    score = models.IntegerField(default=0, verbose_name=_(u"题目总分"))

    testdata_count = models.IntegerField(default=0, verbose_name=_(u"用例数目"))

    testdata_score = models.JSONField(default=list, verbose_name=_(u"用例分数"))

    extra_info = models.JSONField(blank=True, null=True, verbose_name=_(u"其他信息"))

    class Meta:
        db_table = 'problem_judge'
        app_label = 'problem'
        verbose_name = _(u"题目评测信息")
        verbose_name_plural = _(u"题目评测信息列表")


class ProblemInfo(models.Model):
    problem_content = models.ForeignKey(ProblemContent, on_delete=models.CASCADE, verbose_name=_(u"题目描述内容"))

    problem_judge = models.ForeignKey(ProblemJudge, on_delete=models.RESTRICT, verbose_name=_(u"评测信息"))

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
    display_id = models.IntegerField(default=1000, verbose_name=_(u"题目显示编号"))

    title = models.CharField(max_length=512, verbose_name=_(u"标题"))

    time_limit = models.IntegerField(default=1000, verbose_name=_(u"时间限制"))

    memory_limit = models.IntegerField(default=262144, verbose_name=_(u"内存限制"))

    problem_info = models.ForeignKey(ProblemInfo, on_delete=models.RESTRICT, verbose_name=_(u"题目信息"))

    extra_info = models.JSONField(blank=True, null=True, verbose_name=_(u"其他信息"))

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name=_(u"创建者"))

    is_public = models.BooleanField(default=True, verbose_name=_(u"是否公开"),
                                    help_text='该项被选择后，题目将会被所有人看到，如果不选择则题目只能被超级用户和管理员看到.')

    # accepted_number = models.IntegerField(default=0, verbose_name=_(u"通过人数"))
    # submit_number = models.IntegerField(default=0, verbose_name=_(u"提交次数"))
    # level = models.IntegerField(default=3, verbose_name=_(u"题目难度"))

    class Meta:
        db_table = 'problem'
        app_label = 'problem'
        verbose_name = _(u"题目信息")
        verbose_name_plural = _(u"题目列表")


class ProblemRepository(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u"题目仓库名称"))

    is_public = models.BooleanField(default=False, verbose_name=_(u"是否公开"))

    problems = models.ManyToManyField(Problem, verbose_name=_(u"题目列表"))

    objects = PermissionManager()

    def __str__(self):
        if self.name.endswith('题库'):
            return self.name
        else:
            return f'{self.name}题库'

    class Meta:
        db_table = 'problem_repository'
        app_label = 'problem'
        verbose_name = _(u"题目仓库")
        verbose_name_plural = _(u"题目仓库列表")


MAIN_PROBLEM_REPOSITORY = ProblemRepository(name=MAIN_PROBLEM_REPOSITORY_NAME)
