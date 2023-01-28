import re

from django.contrib.auth.models import User, Group
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.constants import NJUST_ICPC_GROUP as NJUST_ICPC_GROUP_NAME
from CaCatHead.core.models import BaseModel

NJUST_ICPC_GROUP = Group(name=NJUST_ICPC_GROUP_NAME)


class UserInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(
        max_length=50, blank=True, default='', verbose_name=_("昵称"))

    rating = models.IntegerField(default=1500, verbose_name=_("Rating"))

    is_teacher = models.BooleanField(default=False, verbose_name=_("是否教师"))

    class Meta:
        db_table = 'user_info'
        verbose_name = _("用户信息")
        verbose_name_plural = _("用户组")


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
