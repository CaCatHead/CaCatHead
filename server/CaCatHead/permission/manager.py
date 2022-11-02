from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Subquery, Q

from CaCatHead.permission.models import UserPermission, GroupPermission


class PermissionManager(models.Manager):
    """
    对象级别权限控制
    注意: 使用该类的表需要有一个布尔字段 is_public 和指向用户的外键 owner
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
        return Q(id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_user_group_private(self, user: User, permissions: [str], **kwargs):
        """
        生成权限查询条件：用户所属的组拥有的权限
        """
        group_subquery = Group.objects.filter(user=user)
        permission_subquery = GroupPermission.objects.filter(group__in=Subquery(group_subquery.values('id')),
                                                             content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_group_private(self, group: Group, permissions: [str], **kwargs):
        """
        生成权限查询条件：组拥有的权限
        """
        permission_subquery = GroupPermission.objects.filter(group=group, content_type=self.model_name())
        if len(permissions) > 0:
            permission_subquery = permission_subquery.filter(codename__in=permissions)
        return Q(id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def filter_user_public(self, user: User, permission: str, **kwargs):
        """
        过滤公开的和用户拥有某权限的数据库实体
        注意：该方法通常只用于读相关的操作，用于写操作会导致任意用户更改公开内容
        """
        if user is None or not user.is_authenticated:
            # 未认证用户只能看到公开内容
            return self.filter_public(**kwargs)
        elif user.is_active and (user.is_superuser or user.is_staff):
            # 超级用户或管理用户, 直接返回
            return self.get_queryset().filter(**kwargs)
        else:
            # 其他用户, 查询用户拥有的权限
            query_user = self._q_user_private(user, [permission], is_public=False)
            query_user_group = self._q_user_group_private(user, [permission], is_public=False)
            return self.get_queryset().filter(Q(**kwargs),
                                              Q(is_public=True) | Q(owner=user) | query_user | query_user_group)

    def filter_user_permission(self, user: User, permission=None, permissions=None, **kwargs):
        """
        使用用户和用户所属的组, 过滤满足权限的数据库实体
        """
        # 列出所需的权限
        if permissions is None:
            permissions = []
        if permission is not None:
            permissions.append(permission)

        if user is None or not user.is_authenticated:
            # 未认证用户什么都看不见
            return self.none()
        elif user.is_active and (user.is_superuser or user.is_staff):
            # 超级用户或管理员用户可以看见一切, 直接返回
            return self.get_queryset().filter(**kwargs)
        else:
            # 其他用户, 查询用户拥有的权限
            query_user = self._q_user_private(user, permissions)
            query_user_group = self._q_user_group_private(user, permissions)
            return self.get_queryset().filter(Q(**kwargs), Q(owner=user) | query_user | query_user_group)

    def grant_user_permission(self, user: User, permission: str, content_id: int):
        """
        赋予用户权限
        """
        user_permission = UserPermission(user=user, content_type=self.model_name(), content_id=content_id,
                                         codename=permission)
        user_permission.save()
        return user_permission

    def revoke_user_permission(self, user: User, permission: str, content_id: int):
        """
        取消用户权限
        """
        user_permissions = UserPermission.objects.filter(user=user,
                                                         content_type=self.model_name(),
                                                         content_id=content_id,
                                                         codename=permission)
        if user_permissions.count() == 0:
            return False
        else:
            user_permissions.delete()
            return True

    def grant_group_permission(self, group: Group, permission: str, content_id: int):
        """
        赋予组权限
        """
        group_permission = GroupPermission(group=group, content_type=self.model_name(), content_id=content_id,
                                           codename=permission)
        group_permission.save()
        return group_permission

    def revoke_group_permission(self, group: Group, permission: str, content_id: int):
        """
        取消组权限
        """
        group_permissions = GroupPermission.objects.filter(group=group,
                                                           content_type=self.model_name(),
                                                           content_id=content_id,
                                                           codename=permission)
        if group_permissions.count() == 0:
            return False
        else:
            group_permissions.delete()
            return True
