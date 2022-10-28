from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase

from CaCatHead.core.tests import init_superuser
from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post


class PostManagerTests(APITestCase):
    # fixtures = ('post.json', )

    @classmethod
    def setUpTestData(cls):
        init_superuser()
        call_command('loaddata', 'CaCatHead/post/fixtures/post.json', app_label='CaCatHead.post')
        user = User.objects.create_user(username='world', email='world@example.com', password='12345678')
        Post.objects.grant_user_permission(user, PostPermissions.Read, 1)
        Post.objects.grant_user_permission(user, PostPermissions.Write, 2)

    def test_posts(self):
        posts = Post.objects.all()
        assert len(posts) == 2
        assert posts[0].title == '系统公告'
        assert posts[1].title == '公告测试'

    def test_query_user_private_posts(self):
        user = User.objects.filter(username='world').first()
        posts = Post.objects.filter_user(user=user)
        assert len(posts) == 2
        public_post, private_post = posts
        assert public_post.id == 1
        assert public_post.title == '系统公告'
        assert public_post.is_public
        assert private_post.id == 2
        assert private_post.title == '公告测试'
        assert not private_post.is_public


class PostViewTests(APITestCase):
    pass
