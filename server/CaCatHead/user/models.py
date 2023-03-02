import re

from django.contrib.auth.models import User, Group
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.constants import NJUST_ICPC_GROUP as NJUST_ICPC_GROUP_NAME
from CaCatHead.core.models import BaseModel

NJUST_ICPC_GROUP = Group(name=NJUST_ICPC_GROUP_NAME)


class UserInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=50, unique=True, blank=True, default='', verbose_name=_("昵称"))

    rating = models.IntegerField(default=None, null=True, verbose_name=_("Rating"))

    rank = models.CharField(default='newbie', max_length=32, verbose_name=_("Rank"))

    is_teacher = models.BooleanField(default=False, verbose_name=_("是否教师"))

    class Meta:
        db_table = 'user_info'
        verbose_name = _("用户信息")
        verbose_name_plural = _("用户组")


class UserToken(models.Model):
    key = models.CharField(_("Key"), max_length=512, primary_key=True)

    user = models.ForeignKey(
        User, related_name='user_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )

    login_ip = models.CharField(max_length=64, verbose_name=_("登录 IP"))

    login_time = models.DateTimeField(auto_now_add=True, verbose_name=_("登录时间"))

    expiry_time = models.DateTimeField(verbose_name=_("过期时间"))

    user_agent = models.CharField(max_length=512, verbose_name=_("登录 User Agent"))

    class Meta:
        db_table = 'user_token'
        verbose_name = _("用户 Token")
        verbose_name_plural = _("用户 Token 列表")

    def is_valid(self):
        return timezone.now() <= self.expiry_time


class StudentInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    student_id = models.CharField(
        max_length=32,
        validators=[validators.RegexValidator(re.compile(r'^\d+$'), 'Enter a valid student id')],
        null=True,
        blank=True,
        default=None,
        verbose_name=_("学号")
    )

    student_name = models.CharField(
        max_length=32, blank=True, verbose_name=_("学生姓名"))

    class_id = models.CharField(
        max_length=32,
        validators=[validators.RegexValidator(re.compile(r'^\d+$'), 'Enter a valid class id')],
        blank=True,
        verbose_name=_("班级编号"))

    student_college = models.CharField(
        max_length=64, blank=True, verbose_name=_("所在学院"))

    student_major = models.CharField(
        max_length=32, blank=True, verbose_name=_("主修专业"))

    student_major_field = models.CharField(
        max_length=32, blank=True, verbose_name=_("专业方向"))

    class Meta:
        db_table = 'student_info'
        verbose_name = _('学生信息')
        verbose_name_plural = _("学生组")
