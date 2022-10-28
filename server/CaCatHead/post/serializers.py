from rest_framework import serializers

from CaCatHead.post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'created', 'updated', 'sort_time', 'title', 'is_public']


class PostContentSerializer(serializers.ModelSerializer):
    content = serializers.SlugRelatedField(read_only=True, slug_field='content')

    class Meta:
        model = Post
        fields = ['id', 'content', 'created', 'updated', 'sort_time', 'title', 'is_public']
