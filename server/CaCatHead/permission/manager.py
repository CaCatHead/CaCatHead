from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Subquery, Q
from knox.models import User

from CaCatHead.permission.models import UserPermission, GroupPermission


class PermissionManager(models.Manager):
    def model_name(self):
        return self.model._meta.model_name

    def filter_public(self, **kwargs):
        query_set = self.get_queryset()
        return query_set.filter(is_public=True, **kwargs)

    def _q_user_private(self, **kwargs):
        assert 'user' in kwargs
        user = kwargs['user']
        permission_subquery = UserPermission.objects.filter(user=user, content_type=self.model_name())
        del kwargs['user']
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def _q_group_private(self, **kwargs):
        assert 'group' in kwargs
        group = kwargs['group']
        permission_subquery = GroupPermission.objects.filter(group=group, content_type=self.model_name())
        del kwargs['group']
        return Q(is_public=False, id__in=Subquery(permission_subquery.values('content_id')), **kwargs)

    def filter_user(self, **kwargs):
        query_user = self._q_user_private(**kwargs)
        return self.get_queryset().filter(Q(is_public=True) | query_user)

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
