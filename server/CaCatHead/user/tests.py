from django.conf import settings
from django.contrib.auth.models import User

from CaCatHead.core.tests import TestCase

ROOT_USER = settings.CACATHEAD_ROOT_USER
ROOT_PASS = settings.CACATHEAD_ROOT_PASS
DEFAULT_EMAIL = 'root@example.com'

ROOT_PROFILE = {'id': 1, 'username': 'root', 'nickname': 'root', 'email': 'root@example.com', 'polygon': True}


WORLD_PROFILE = {'id': 2, 'username': 'world', 'nickname': 'world', 'email': 'world@example.com','polygon': False}

WORLD_INFO = {"username": "world", "email": "world@example.com", "password": "12345678"}

def login_token_valid(resp):
    return len(resp.data['expiry']) > 0 and len(resp.data['token']) > 0


class UserAuthTests(TestCase):
    def test_hello_world(self):
        resp = self.client.get('/api/ping')
        assert resp.status_code == 200
        assert resp.data['status'] == 'ok'
        assert resp.data['message'] == 'Hello, world!'
        self.assertMatchSnapshot(resp.data)

    def test_login(self):
        resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": ROOT_PASS})
        assert resp.status_code == 200
        assert login_token_valid(resp)
        # 测试 Token 访问 /api/user/profile 返回 200
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        assert resp2.status_code == 200
        self.assertEqual(resp2.data, {'status': 'ok', 'user': ROOT_PROFILE})

    def test_token_error_authentication_fail(self):
        resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": ROOT_PASS})
        assert resp.status_code == 200
        assert login_token_valid(resp)
        # 随便搞一个 token 访问 /api/user/profile 返回 401
        authorization = resp.data['token']
        authorization = "Token " + authorization[::-1]
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        self.assertEqual(resp2.status_code, 401)

    def test_password_error(self):
        resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": "gdxtxdy"})
        assert resp.status_code == 401
        self.assertEqual(resp.data['detail'], "不正确的身份认证信息。")

    def test_username_error(self):
        resp = self.client.post('/api/auth/login', {"username": "gdx", "password": "gdxtxdy"})
        assert resp.status_code == 401
        assert resp.data['detail'] == "不正确的身份认证信息。"

    def test_sql_inject_fail(self):
        """
        TODO: SQL injection failure
        """
        resp = self.client.post('/api/auth/login',
                                {"username": "root; DELETE FROM auth_user", "password": "12345678"})

    def test_multi_login_logout(self):
        """
        多次登录, 登录了带 token, 第二次登录返回已登录
        """
        resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": ROOT_PASS})
        assert resp.status_code == 200
        assert login_token_valid(resp)
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.post('/api/auth/login',
                                 {"username": ROOT_USER, "password": ROOT_PASS})
        assert resp2.status_code == 401
        assert resp2.data['detail'] == '你已经登陆过了'
        resp3 = self.client.post('/api/auth/logout')
        assert resp3.status_code == 204
        resp4 = self.client.post('/api/user/profile')
        assert resp4.status_code == 401
        assert resp4.data['detail'] == "认证令牌无效。"

    def test_multi_login_logoutall(self):
        """
        多次登录 不带token 每个独立 全部退出
        """
        authorizations = []
        # 多次登录
        for _ in range(0, 10):
            resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": ROOT_PASS})
            assert resp.status_code == 200
            assert login_token_valid(resp)
            authorizations.append("Token " + resp.data['token'])
        # 每个 token 查看信息
        for authorization in authorizations:
            self.client.credentials(HTTP_AUTHORIZATION=authorization)
            resp2 = self.client.get('/api/user/profile')
            assert resp2.status_code == 200
            self.assertEqual(resp2.data, {'status': 'ok', 'user': ROOT_PROFILE})
        # 退出
        self.client.credentials(HTTP_AUTHORIZATION=authorizations[0])
        resp3 = self.client.post('/api/auth/logoutall')
        assert resp3.status_code == 204
        # 认证 token 无效
        for authorization in authorizations:
            self.client.credentials(HTTP_AUTHORIZATION=authorization)
            resp2 = self.client.get('/api/user/profile')
            assert resp2.status_code == 401
            assert resp2.data['detail'] == "认证令牌无效。"

    def test_flow(self):
        """
        测试整个流程 注册-登录-查看-退出
        """
        # 注册
        resp = self.client.post('/api/auth/register', WORLD_INFO)
        assert resp.status_code == 200
        self.assertEqual(resp.data['user'], WORLD_PROFILE)
        user = User.objects.get(username='world')
        username = user.username
        email = user.email
        assert username == 'world'
        assert email == 'world@example.com'
        # 登录
        resp = self.client.post('/api/auth/login',
                                {"username": username, "password": "12345678"})
        assert resp.status_code == 200
        assert login_token_valid(resp)
        # 查看信息
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        assert resp2.status_code == 200
        self.assertEqual(resp2.data, {'status': 'ok', 'user': WORLD_PROFILE})
        # 退出
        resp3 = self.client.post('/api/auth/logout')
        assert resp3.status_code == 204

    def test_login_validate_error(self):
        resp = self.client.post('/api/auth/login', {
            "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        })
        assert resp.status_code == 400
        assert resp.data['username'][0] == "请确保这个字段不能超过 64 个字符。"
        assert resp.data['password'][0] == "请确保这个字段不能超过 64 个字符。"

    def test_logout_token_fail(self):
        """
        登录获取 token，退出，该 token 不可用
        """
        resp = self.client.post('/api/auth/login', {"username": ROOT_USER, "password": ROOT_PASS})
        assert resp.status_code == 200
        assert login_token_valid(resp)
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.post('/api/auth/logout')
        assert resp2.status_code == 204
        resp3 = self.client.post('/api/user/profile')
        assert resp3.status_code == 401
        assert resp3.data['detail'] == "认证令牌无效。"


class UserRegisterTests(TestCase):
    def assertUserRegistered(self, username='world', email='world@example.com'):
        user = User.objects.get(username=username)
        assert user.username == username
        assert user.email == email

    def test_register(self):
        """
        正常注册
        """
        resp = self.client.post('/api/auth/register', WORLD_INFO)
        assert resp.status_code == 200
        self.assertEqual(resp.data['user'], WORLD_PROFILE)
        self.assertUserRegistered('world', 'world@example.com')

    def test_register_validate_error(self):
        resp = self.client.post('/api/auth/register', {
            "username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        })
        assert resp.status_code == 400
        assert resp.data['username'][0] == "请确保这个字段不能超过 64 个字符。"
        assert resp.data['password'][0] == "请确保这个字段不能超过 64 个字符。"

    def test_register_error_same_username(self):
        """
        同一个用户名多次注册
        """
        # 注册
        resp = self.client.post('/api/auth/register', {
            "username": "world",
            "email": "world@example.com",
            "password": "12345678"
        })
        assert resp.status_code == 200
        self.assertEqual(resp.data['user'], WORLD_PROFILE)
        self.assertUserRegistered('world', 'world@example.com')
        # 二次注册
        resp2 = self.client.post('/api/auth/register', {
            "username": "world",
            "email": "gdx@example.com",
            "password": "12345678"
        })
        assert resp2.data['detail'] == '用户名 world 已经被注册'

    def test_register_ok_same_email(self):
        """
        同一个邮箱多次注册
        """
        # 注册
        resp = self.client.post('/api/auth/register', WORLD_INFO)
        assert resp.status_code == 200
        self.assertEqual(resp.data['user'], WORLD_PROFILE)
        self.assertUserRegistered('world', 'world@example.com')
        # 二次注册
        self.client.post('/api/auth/register', {
            "username": "gdx",
            "email": "world@example.com",
            "password": "12345678"
        })
        self.assertUserRegistered('world', 'world@example.com')
        self.assertUserRegistered('gdx', 'world@example.com')
