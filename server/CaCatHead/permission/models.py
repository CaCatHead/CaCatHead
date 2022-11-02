from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserPermission(models.Model):
    """用户权限
    user: 用户
    content_type: 资源类型
    content_id: 资源 id
    codename: 权限内容
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(u"用户"))

    content_type = models.CharField(max_length=32, verbose_name=_(u"资源类型"))

    content_id = models.BigIntegerField(verbose_name=_(u"资源 id"))

    codename = models.CharField(max_length=32, verbose_name=_(u"权限内容"))

    class Meta:
        db_table = 'user_permission'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'content_type', 'content_id', 'codename'],
                name='unique user_permission')
        ]


class GroupPermission(models.Model):
    """组权限
    group: 组
    content_type: 资源类型
    content_id: 资源 id
    codename: 权限内容
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_(u"组"))

    content_type = models.CharField(max_length=32, verbose_name=_(u"资源类型"))

    content_id = models.BigIntegerField(verbose_name=_(u"资源 id"))

    codename = models.CharField(max_length=32, verbose_name=_(u"权限内容"))

    class Meta:
        db_table = 'group_permission'
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'content_type', 'content_id', 'codename'],
                name='unique group_permission')
        ]
