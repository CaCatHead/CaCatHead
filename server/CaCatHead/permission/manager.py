from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Subquery, Q
from knox.models import User

from CaCatHead.permission.models import UserPermission, GroupPermission


class PermissionManager(models.Manager):
    """
    对象级别权限控制
    """

    def model_name(self):
        return self.model._meta.model_name

    def filter_public(self, **kwargs):
        query_set = self.get_queryset()
        return query_set.filter(is_public=True, **kwargs)

    def _q_user_private(self, user: User, permissions: [str], **kwargs):
        permission_subquery = UserPermission.objects.filter(user=user, content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_group_private(self, group: Group, permissions: [str], **kwargs):
        permission_subquery = GroupPermission.objects.filter(group=group, content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def filter_user(self, **kwargs):
        assert 'user' in kwargs
        user = kwargs['user']

        # 列出所需的权限
        permissions = []
        if 'permission' in kwargs:
            permissions.append(kwargs['permission'])
            kwargs.pop('permission', None)
        if 'permissions' in kwargs:
            for p in kwargs['permissions']:
                permissions.append(p)
            kwargs.pop('permissions', None)

        # 清空 filter 无关的参数
        kwargs.pop('user', None)
        kwargs.pop('group', None)
        kwargs.pop('groups', None)

        if user is None or not user.is_authenticated:
            # 未认证用户只能看到公开内容
            return self.filter_public(**kwargs)
        elif user.is_active and (user.is_superuser or user.is_staff):
            # 超级用户或管理用户, 直接返回
            return self.get_queryset().filter(**kwargs)
        else:
            # 其他用户, 查询用户拥有的权限
            query_user = self._q_user_private(user, permissions, **kwargs)
            return self.get_queryset().filter(Q(**kwargs), Q(is_public=True) | query_user)

    def grant_user_permission(self, user: User, permission: str, content_id):
        user_permission = UserPermission(user=user, content_type=self.model_name(), content_id=content_id,
                                         codename=permission)
        user_permission.save()
        return user_permission

    def grant_group_permission(self, group: Group, permission: str, content_id):
        group_permission = GroupPermission(group=group, content_type=self.model_name(), content_id=content_id,
                                           codename=permission)
        group_permission.save()
        return group_permission
