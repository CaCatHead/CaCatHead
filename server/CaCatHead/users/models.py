import re

from django.db import models
from django.utils import timezone
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

from CaCatHead.core.models import BaseModel


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


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=30,
                                unique=True,
                                validators=[
                                    validators.RegexValidator(re.compile(r'^[\w.@+-]+$'), 'Enter a valid username.',
                                                              'invalid')],
                                verbose_name=_("用户名"))

    nickname = models.CharField(
        max_length=50, blank=True, default='', verbose_name=_("昵称"))

    email = models.EmailField(blank=True, verbose_name=_("电子邮件"))

    is_active = models.BooleanField(default=True,
                                    verbose_name=_("是否可用"),
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')

    is_teacher = models.BooleanField(default=False, verbose_name=_("是否教师"))

    is_staff = models.BooleanField(default=False, verbose_name=_("管理员"))

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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def gravatar_url(self, size=460):
        # url = "http://gravatar.com/avatar/" + \
        #     hashlib.md5(self.email.lower()).hexdigest() + "?"
        # url += urllib.parse.urlencode({'s': str(size)})
        # Use the default avatar
        return 'https://www.gravatar.com/avatar'

    def gravatar_url_40(self):
        return self.gravatar_url(size=40)

    def gravatar_url_460(self):
        return self.gravatar_url(size=460)

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['student_id']
        verbose_name = _("用户")
        verbose_name_plural = _("用户组")

    __rbac_backend = None
    __userPerms = None

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # def get_all_roles(self):
    #     from rbac.models import RbacRole
    #     return RbacRole.objects.filter(rbacuserassignment__user=self)

    # def get_all_permissions(self, obj=None):
    #     if not self.__rbac_backend:
    #         from rbac.backends import RbacUserBackend
    #         self.__rbac_backend = RbacUserBackend()
    #     return self.__rbac_backend.get_all_permissions(self, obj)

    # def has_perm(self, perm, obj=None):
    #     if self.is_superuser or self.is_staff:
    #         return True
    #     if not self.__rbac_backend:
    #         from rbac.backends import RbacUserBackend
    #         self.__rbac_backend = RbacUserBackend()
    #     return self.__rbac_backend.has_perm(self, perm, obj)

    # def has_role_perm(self, role, perm, obj=None):
    #     if self.is_superuser or self.is_staff:
    #         return True
    #     if not self.__rbac_backend:
    #         from rbac.backends import RbacUserBackend
    #         self.__rbac_backend = RbacUserBackend()
    #     return self.__rbac_backend.has_role_perm(self, role, perm, obj)

    # def has_role(self, role, obj=None):
    #     if self.is_superuser or self.is_staff:
    #         return True
    #     if not self.__rbac_backend:
    #         from rbac.backends import RbacUserBackend
    #         self.__rbac_backend = RbacUserBackend()
    #     return self.__rbac_backend.has_role(self, role)

    def has_perms(self, perm_list, obj=None):
        if self.is_superuser or self.is_staff:
            return True
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    @classmethod
    def get_users_student_name(cls, username_list):
        username_student_name = User.objects.filter(
            username__in=username_list).values_list("username", "student_name")
        student_name_list = {}
        for user in username_student_name:
            student_name_list[user[0]] = user[1]
        return student_name_list
