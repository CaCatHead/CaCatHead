from django.contrib.auth.models import User

from CaCatHead.core.tests import TestCase
from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post
from CaCatHead.user.tests import ROOT_USER

POST1_INFO = {'id': 1, 'owner': {'id': 1, 'username': 'root', 'nickname': 'root'}, 'content': '你好！',
              'created': '2022-10-27T02:20:03.089000+08:00', 'updated': '2022-10-27T02:20:03.089000+08:00',
              'sort_time': '2022-10-27T02:20:03.089000+08:00', 'title': '系统公告', 'is_public': True}


class PostManagerTests(TestCase):
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


class PostViewTests(TestCase):
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


    def user_login(self, user: User):
        # 用户登陆
        resp = self.client.post('/api/auth/login', {"username": user.username, "password": '12345678'})
        assert resp.status_code == 200
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

    def visitor_view_post(self, post_id: int):
        # 游客直接请求公告
        return self.client.get(f'/api/post/{post_id}')

    def visitor_list_posts(self):
        # 游客列出公告列表
        return self.client.get(f'/api/posts')

    def visitor_list_public_posts(self):
        # 游客列出公开公告列表
        return self.client.get(f'/api/posts/public')

    def user_view_post(self, user: User, post_id: int):
        # 用户请求公告
        self.user_login(user)
        return self.client.get(f'/api/post/{post_id}')

    def user_list_posts(self, user: User):
        # 用户列出公告列表
        self.user_login(user)
        return self.client.get(f'/api/posts')

    def user_list_public_posts(self, user: User):
        # 用户列出公开公告列表
        self.user_login(user)
        return self.client.get(f'/api/posts/public')

    def test_superuser_view_public_post(self):
        resp = self.user_view_post(self.root, 1)
        assert resp.status_code == 200
        post = resp.data['post']
        assert post['is_public']
        self.assertEqual(post, POST1_INFO)
        # assert resp body, this may be wrapped with another method

    def test_superuser_view_private_post(self):
        resp = self.user_view_post(self.root, 2)
        assert resp.status_code == 200
        post = resp.data['post']
        assert post['is_public'] == False

    def test_superuser_view_nonexistence_post(self):
        resp = self.user_view_post(self.root, 999)
        assert resp.status_code == 404
        assert resp.data['detail'] == "公告未找到"

    def test_admin_view_public_post(self):
        resp = self.user_view_post(self.admin, 1)
        assert resp.status_code == 200
        post = resp.data['post']
        assert post['is_public']

    def test_admin_view_private_post(self):
        resp = self.user_view_post(self.root, 2)
        assert resp.status_code == 200
        post = resp.data['post']
        assert post['is_public'] == False

    def test_admin_view_nonexistence_post(self):
        resp = self.user_view_post(self.root, 999)
        assert resp.status_code == 404
        assert resp.data['detail'] == "公告未找到"

    def test_guest_view_public_post(self):
        resp = self.visitor_list_public_posts()
        posts = resp.data['posts']
        for post in posts:
            assert post['is_public']
        assert resp.status_code == 200

    def test_guest_view_private_post(self):
        resp = self.visitor_view_post(2)
        assert resp.status_code == 404
        assert resp.data['detail'] == "公告未找到"
        resp1 = self.user_view_post(self.root, 2)
        assert resp1.status_code == 200
        post = resp1.data['post']
        assert post['is_public'] == False

    def test_guest_view_nonexistence_post(self):
        resp = self.visitor_view_post(999)
        assert resp.status_code == 404
        assert resp.data['detail'] == "公告未找到"
        resp1 = self.user_view_post(self.root, 999)
        assert resp1.status_code == 404

