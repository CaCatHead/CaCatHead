from django.core.management import call_command
from rest_framework.test import APITestCase

from CaCatHead.core.tests import init_superuser
from CaCatHead.post.models import Post


class PostTests(APITestCase):
    # fixtures = ('post.json', )

    @classmethod
    def setUpTestData(cls):
        init_superuser()
        call_command('loaddata', 'CaCatHead/post/fixtures/post.json', app_label='CaCatHead.post')

    def test_posts(self):
        posts = Post.objects.all()
        assert len(posts) == 2
        assert posts[0].title == '系统公告'
        assert posts[1].title == '公告测试'
