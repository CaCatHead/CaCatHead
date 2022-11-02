from rest_framework import serializers

from CaCatHead.permission.models import UserPermission, GroupPermission


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ['user_id', 'content_type', 'content_id', 'codename']


class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermission
        fields = ['group_id', 'content_type', 'content_id', 'codename']
