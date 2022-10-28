from django.db import models
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.models import BaseModel


class ProblemModel(BaseModel):
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

    class Meta:
        db_table = 'problems'
        app_label = 'problem'
        verbose_name = _(u"题目信息")
        verbose_name_plural = _(u"题目列表")

    repo = models.CharField(max_length=20, default='cppexam', blank=False, verbose_name=_(u"题目类型"))
    label = models.CharField(max_length=45, unique=True, null=True, verbose_name=_(u"题目编号"))
    title = models.CharField(max_length=500, verbose_name=_(u"标题"))
    description = models.TextField(blank=True, null=True, verbose_name=_(u"题目描述"))
    inputdescription = models.TextField(blank=True, null=True, verbose_name=_(u"输入描述"))
    outputdescription = models.TextField(blank=True, null=True, verbose_name=_(u"输出描述"))
    inputsample = models.TextField(blank=True, null=True, verbose_name=_(u"输入样例"))
    outputsample = models.TextField(blank=True, null=True, verbose_name=_(u"输出样例"))
    hint = models.TextField(blank=True, null=True, verbose_name=_(u"解答提示"))
    source = models.TextField(blank=True, null=True, verbose_name=_(u"题目来源"))
    timelimit = models.IntegerField(default=1000, verbose_name=_(u"时间限制"))
    memorylimit = models.IntegerField(default=262144, verbose_name=_(u"内存限制"))
    # accepted_number = models.IntegerField(default=0, verbose_name=_(u"通过人数"))
    # submit_number = models.IntegerField(default=0, verbose_name=_(u"提交次数"))
    score = models.IntegerField(default=0, verbose_name=_(u"题目总分"))
    level = models.IntegerField(default=3, verbose_name=_(u"题目难度"))
    testdata_count = models.IntegerField(default=0, verbose_name=_(u"用例数目"))
    testdata_score = models.TextField(blank=True, null=True, verbose_name=_(u"用例分数"))
    # create_user = models.CharField(max_length=45, default='admin', null=True, verbose_name=_(u"创建者"))
    is_public = models.BooleanField(default=True, verbose_name=_(u"是否公开"),
                                    help_text='该项被选择后，题目将会被所有人看到，如果不选择则题目只能被超级用户和管理员看到.')

    # @classmethod
    # def get_all_create_user_nicename(cls):
    #     create_usernames = cls.objects.values_list("create_user", flat=True)
    #     nicename_list = User.get_users_student_name(create_usernames)
    #     return nicename_list
    #
    # @classmethod
    # def get_all_problem_repo(cls):
    #     label_repo_list = cls.objects.values_list('label', 'repo')
    #     repo_list = {}
    #     for label_repo in label_repo_list:
    #         repo_list[label_repo[0]] = label_repo[1]
    #     return repo_list
