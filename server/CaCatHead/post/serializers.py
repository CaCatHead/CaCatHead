from rest_framework import serializers
from rest_framework.exceptions import NotFound

from CaCatHead.post.models import Post
from CaCatHead.user.serializers import UserSerializer


class BasePostSerializer(serializers.ModelSerializer):
    def get_or_raise(self):
        """
        检查待序列化的 Post 对象是否为空, 抛出 404
        """
        if self.instance is not None:
            return self.data
        else:
            raise NotFound(detail='公告未找到')


class PostSerializer(BasePostSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'created', 'updated', 'sort_time', 'title', 'is_public']


class PostContentSerializer(BasePostSerializer):
    content = serializers.SlugRelatedField(read_only=True, slug_field='content')

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'content', 'created', 'updated', 'sort_time', 'title', 'is_public']
