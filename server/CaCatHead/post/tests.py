from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post
from CaCatHead.user.tests import ROOT_USER


class PostManagerTests(APITestCase):
    fixtures = ('post.json',)

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='world', email='world@example.com', password='12345678')
        Post.objects.grant_user_permission(user, PostPermissions.Read, 1)
        Post.objects.grant_user_permission(user, PostPermissions.Read, 2)

    def test_posts(self):
        posts = Post.objects.all()
        assert len(posts) == 2
        assert posts[0].title == '系统公告'
        assert posts[1].title == '公告测试'

    def test_query_user_posts(self):
        user = User.objects.filter(username='world').first()
        posts = Post.objects.filter_user_public(user=user, permission=PostPermissions.Read)
        assert len(posts) == 2
        public_post, private_post = posts
        assert public_post.id == 1
        assert public_post.title == '系统公告'
        assert public_post.is_public
        assert private_post.id == 2
        assert private_post.title == '公告测试'
        assert not private_post.is_public


class PostViewTests(APITestCase):
    fixtures = ('post.json',)

    @classmethod
    def setUpTestData(cls):
        cls.root = User.objects.get(username=ROOT_USER)

        admin = User.objects.create_user(username='admin', email='admin@example.com', password='12345678')
        admin.is_staff = True
        admin.save()
        cls.admin = admin

        user = User.objects.create_user(username='world', email='world@example.com', password='12345678')
        user.save()
        cls.user = user

    def base_view_post(self, user: User, post_id: int):
        # 用户登陆
        resp = self.client.post('/api/auth/login', {"username": user.username, "password": '12345678'})
        assert resp.status_code == 200
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

        return self.client.get(f'/api/post/{post_id}')

    def test_superuser_view_public_post(self):
        resp = self.base_view_post(self.root, 1)
        assert resp.status_code == 200
        # assert resp body, this may be wrapped with another method
