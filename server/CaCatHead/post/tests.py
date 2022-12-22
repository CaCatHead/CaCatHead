from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from CaCatHead.core.constants import NJUST_ICPC_GROUP as NJUST_ICPC_GROUP_NAME
from CaCatHead.core.tests import TestCase
from CaCatHead.permission.constants import PostPermissions
from CaCatHead.post.models import Post
from CaCatHead.user.tests import ROOT_USER

Error_INFO_404 = '公告未找到'


class PostManagerTests(TestCase):
    fixtures = ('post.json',)

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='world', email='world@example.com', password='12345678')
        user.save()
        cls.user = user
        Post.objects.grant_user_permission(user, PostPermissions.Read, 1)
        Post.objects.grant_user_permission(user, PostPermissions.Read, 2)
        my_group = Group.objects.filter(name=NJUST_ICPC_GROUP_NAME).first()
        my_group.user_set.add(user)
        cls.group = my_group

    def user_login(self, user: User):
        # 用户登陆
        resp = self.client.post('/api/auth/login', {"username": user.username, "password": '12345678'})
        assert resp.status_code == 200
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

    def user_view_post(self, post_id: int):
        # 用户请求公告
        return self.client.get(f'/api/post/{post_id}')

    def test_posts(self):
        posts = Post.objects.all()
        assert len(posts) == 2
        assert posts[0].title == '系统公告'
        assert posts[1].title == '公告测试'

    def test_query_user_posts(self):
        posts = Post.objects.filter_user_public(user=self.user, permission=PostPermissions.Read)
        assert len(posts) == 2
        public_post, private_post = posts
        assert public_post.id == 1
        assert public_post.title == '系统公告'
        assert public_post.is_public
        assert private_post.id == 2
        assert private_post.title == '公告测试'
        assert not private_post.is_public

    def test_query_user_public_posts(self):
        posts = Post.objects.filter_public()
        self.assertMatchSnapshot(posts)

    def test_query_user_group_read_posts(self):
        user = self.user
        my_group = self.group
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        posts = Post.objects.filter_user_public(user=user, permission=PostPermissions.Read)
        self.assertMatchSnapshot(posts)
        Post.objects.grant_group_permission(my_group, PostPermissions.Read, 2)
        posts = Post.objects.filter_user_public(user=user, permission=PostPermissions.Read)
        self.assertMatchSnapshot(posts)

    def test_query_user_group_only_edit_post(self):
        user = self.user
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        Post.objects.grant_group_permission(self.group, PostPermissions.Edit, 2)
        self.user_login(user)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404

    def test_query_user_private_unread_post(self):
        user = self.user
        self.user_login(user)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404

    def test_query_user_private_only_edit_post(self):
        user = self.user
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        Post.objects.grant_user_permission(user, PostPermissions.Edit, 2)
        self.user_login(user)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404

    def test_query_user_nonexistence_post(self):
        user = self.user
        self.user_login(user)
        resp = self.user_view_post(post_id=999)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        resp = self.user_view_post(post_id=-1)
        assert resp.status_code == 404
        # HttpResponseNotFound

    def test_revoke_group_permission(self):
        user = self.user
        self.user_login(user)
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        my_group = self.group
        Post.objects.grant_group_permission(my_group,PostPermissions.Read,2)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)
        Post.objects.revoke_group_permission(my_group,PostPermissions.Read,2)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404

    def test_revoke_user_permission(self):
        user = self.user
        self.user_login(user)
        Post.objects.revoke_user_permission(user, PostPermissions.Read, 2)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404


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

    def user_view_post(self, post_id: int):
        # 用户请求公告
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
        self.user_login(self.root)
        resp = self.user_view_post(post_id=1)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)
        # assert resp body, this may be wrapped with another method

    def test_superuser_view_private_post(self):
        self.user_login(self.root)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_superuser_view_list_posts(self):
        resp = self.user_list_posts(self.root)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_admin_view_list_posts(self):
        resp = self.user_list_posts(self.admin)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_user_view_list_posts(self):
        resp = self.user_list_posts(self.user)
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_guest_view_list_posts(self):
        resp = self.visitor_list_posts()
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_public_view_list_posts(self):
        resp = self.visitor_list_public_posts()
        assert resp.status_code == 200
        self.assertMatchSnapshot(resp.content)

    def test_superuser_view_nonexistence_post(self):
        self.user_login(self.root)
        resp = self.user_view_post(post_id=999)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        resp = self.user_view_post(post_id=-1)
        assert resp.status_code == 404
        # HttpResponseNotFound

    def test_admin_view_public_post(self):
        self.user_login(self.admin)
        resp = self.user_view_post(post_id=1)
        assert resp.status_code == 200
        post = resp.data['post']
        assert post['is_public']
        self.assertMatchSnapshot(resp.content)

    def test_admin_view_private_post(self):
        self.user_login(self.admin)
        resp = self.user_view_post(post_id=2)
        assert resp.status_code == 200
        post = resp.data['post']
        assert not post['is_public']
        self.assertMatchSnapshot(resp.content)

    def test_admin_view_nonexistence_post(self):
        self.user_login(self.admin)
        resp = self.user_view_post(post_id=999)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        resp = self.user_view_post(post_id=-1)
        assert resp.status_code == 404
        # HttpResponseNotFound

    def test_guest_view_public_post(self):
        resp = self.visitor_list_public_posts()
        posts = resp.data['posts']
        for post in posts:
            assert post['is_public']
        assert resp.status_code == 200

    def test_guest_view_private_post(self):
        resp = self.visitor_view_post(2)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        self.user_login(self.root)
        resp1 = self.user_view_post(post_id=2)
        assert resp1.status_code == 200
        self.assertMatchSnapshot(resp.content)
        assert not post['is_public']

    def test_guest_view_nonexistence_post(self):
        resp = self.visitor_view_post(999)
        assert resp.status_code == 404
        assert resp.data['detail'] == Error_INFO_404
        self.user_login(self.root)
        resp1 = self.user_view_post(post_id=999)
        assert resp1.status_code == 404
