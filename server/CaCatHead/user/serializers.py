from django.contrib.auth.models import User
from rest_framework import serializers

from CaCatHead.core.constants import Permissions
from CaCatHead.user.models import UserInfo


class LoginPayloadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=64)


class RegisterPayloadSerializer(LoginPayloadSerializer):
    email = serializers.EmailField()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['nickname']


class UserSerializer(serializers.BaseSerializer):
    def to_representation(self, user: User):
        user_info = UserInfo.objects.get(user=user)
        return {
            'id': user.id,
            'username': user.username,
            'nickname': user_info.nickname
        }


class FullUserSerializer(serializers.BaseSerializer):
    def to_representation(self, user: User):
        user_info = UserInfo.objects.get(user=user)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'nickname': user_info.nickname,
            'permissions': {
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'polygon': user.has_perm(Permissions.POLYGON),
                'add_post': user.has_perm('post.add_post'),
                'add_contest': user.has_perm('contest.add_contest')
            }
        }
