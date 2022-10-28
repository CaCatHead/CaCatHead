from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Subquery, Q

from CaCatHead.permission.models import UserPermission, GroupPermission


class PermissionManager(models.Manager):
    """
    对象级别权限控制
    注意：使用该类的表需要有一个布尔字段 is_public
    """

    def model_name(self):
        return self.model._meta.model_name

    def filter_public(self, **kwargs):
        """
        过滤公开的数据库对象
        """
        query_set = self.get_queryset()
        return query_set.filter(is_public=True, **kwargs)

    def _q_user_private(self, user: User, permissions: [str], **kwargs):
        """
        生成权限查询条件：用户直接拥有的权限
        """
        permission_subquery = UserPermission.objects.filter(user=user, content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_user_group_private(self, user: User, permissions: [str], **kwargs):
        """
        生成权限查询条件：用户所属的组拥有的权限
        """
        group_subquery = Group.objects.filter(user=user)
        permission_subquery = GroupPermission.objects.filter(group__in=Subquery(group_subquery.values('id')),
                                                             content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_group_private(self, group: Group, permissions: [str], **kwargs):
        """
        生成权限查询条件：组拥有的权限
        """
        permission_subquery = GroupPermission.objects.filter(group=group, content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def filter_user(self, **kwargs):
        """
        使用用户和用户所属的组, 过滤满足权限的数据库实体
        """
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
            query_user_group = self._q_user_group_private(user, permissions, **kwargs)
            return self.get_queryset().filter(Q(**kwargs), Q(is_public=True) | query_user | query_user_group)

    def grant_user_permission(self, user: User, permission: str, content_id):
        """
        赋予用户权限
        """
        user_permission = UserPermission(user=user, content_type=self.model_name(), content_id=content_id,
                                         codename=permission)
        user_permission.save()
        return user_permission

    def grant_group_permission(self, group: Group, permission: str, content_id):
        """
        赋予组权限
        """
        group_permission = GroupPermission(group=group, content_type=self.model_name(), content_id=content_id,
                                           codename=permission)
        group_permission.save()
        return group_permission
