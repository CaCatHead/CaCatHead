import re

from django.contrib.auth.models import User, Group, BaseUserManager
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.models import BaseModel
from CaCatHead.core.constants import NJUST_ICPC_GROUP as NJUST_ICPC_GROUP_NAME


NJUST_ICPC_GROUP = Group(name=NJUST_ICPC_GROUP_NAME)


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.student_id = username
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

    def get_user_by_id(self, uid):
        return self.filter(id=uid)

    def del_user_by_id(self, uid):
        user = self.filter(id=uid)
        user.is_active = False
        user.save()

    def change_username_by_id(self, uid, username):
        user = self.filter(id=uid)
        user.username = username
        user.save()
        return user

    def change_email_by_id(self, uid, email):
        user = self.filter(id=uid)
        user.email = email
        user.save()
        return user

    def change_password_by_id(self, uid, raw_password):
        user = self.filter(id=uid)
        user.set_password(raw_password)
        user.save()
        return user


class UserInfo(BaseModel):
    class Meta:
        verbose_name = _("用户信息")
        verbose_name_plural = _("用户组")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(
        max_length=50, blank=True, default='', verbose_name=_("昵称"))

    is_teacher = models.BooleanField(default=False, verbose_name=_("是否教师"))


class StudentInfo(BaseModel):
    class Meta:
        verbose_name = _('学生信息')
        verbose_name_plural = _("学生组")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    student_id = models.CharField(
        max_length=30,
        validators=[validators.RegexValidator(re.compile(r'^\d+$'), 'Enter a valid student id')],
        null=True,
        blank=True,
        default=None,
        verbose_name=_("学号")
    )

    student_name = models.CharField(
        max_length=40, blank=True, verbose_name=_("学生姓名"))

    class_id = models.CharField(
        max_length=30,
        validators=[validators.RegexValidator(re.compile(r'^\d+$'), 'Enter a valid class id')],
        blank=True,
        verbose_name=_("班级编号"))

    student_college = models.CharField(
        max_length=40, blank=True, verbose_name=_("所在学院"))

    student_major = models.CharField(
        max_length=40, blank=True, verbose_name=_("主修专业"))

    student_major_field = models.CharField(
        max_length=40, blank=True, verbose_name=_("专业方向"))
