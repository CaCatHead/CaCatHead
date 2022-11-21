from rest_framework import serializers

from CaCatHead.permission.models import UserPermission, GroupPermission
from CaCatHead.user.serializers import UserSerializer


class UserPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserPermission
        fields = ['user', 'content_type', 'content_id', 'codename']


class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermission
        fields = ['group_id', 'content_type', 'content_id', 'codename']
