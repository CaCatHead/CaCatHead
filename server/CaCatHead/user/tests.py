import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User


def init_superuser(username='root', password='12345678', email='root@example.com'):
    User.objects.create_superuser(username=username, email=email, password=password)


class UserAuthTests(APITestCase):
    def test_hello_world(self):
        resp = self.client.get('/api/hello/')
        assert resp.status_code == 200
        assert resp.data['message'] == 'Hello, world!'

    def test_login(self):
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "root", "password": "12345678"},
                                format='json')
        assert resp.status_code == 200
        assert len(resp.data['expiry']) > 0
        assert len(resp.data['token']) > 0
        # 测试Token访问/api/user/profile 返回200
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        assert resp2.status_code == 200
        self.assertEqual(resp2.data, {'status': 'ok', 'user': {'username': 'root', 'email': 'root@example.com'}})

    def test_tokenError_authentication_fail(self):
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "root", "password": "12345678"},
                                format='json')
        assert resp.status_code == 200
        assert len(resp.data['expiry']) > 0
        assert len(resp.data['token']) > 0
        # 随便搞一个token访问/api/user/profile 返回401
        authorization = resp.data['token']
        authorization = "Token " + authorization[::-1]
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        self.assertEqual(resp2.status_code, 401)

    def test_password_error(self):
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "root", "password": "gdxtxdy"},
                                format='json')
        assert resp.status_code == 401
        self.assertEqual(resp.data['detail'], "不正确的身份认证信息。")

    def test_username_error(self):
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "gdx", "password": "gdxtxdy"},
                                format='json')
        assert resp.status_code == 401
        assert resp.data['detail'] == "不正确的身份认证信息。"

    def test_sql_inject_fail(self):
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "root; DELETE FROM User", "password": "12345678"},
                                format='json')

    # TODO: SQL injection failure
    def test_register(self):
        resp = self.client.post('/api/auth/register', {
            "username": "world",
            "email": "world@example.com",
            "password": "12345678"
        })
        assert resp.status_code == 200
        self.assertEqual(resp.data['user'], {'username': 'world', 'email': 'world@example.com'})
        Object = User.objects.get(username='world')
        username = Object.username
        email = Object.email
        assert username == 'world'
        assert email == 'world@example.com'

    def test_logout_token_fail(self):  # 登录获取 token，退出，该 token 不可用
        init_superuser()
        resp = self.client.post('/api/auth/login', {"username": "root", "password": "12345678"},
                                format='json')
        assert resp.status_code == 200
        assert len(resp.data['expiry']) > 0
        assert len(resp.data['token']) > 0
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.post('/api/auth/logout')
        assert resp2.status_code == 204
        resp3 = self.client.post('/api/user/profile')
        assert resp3.status_code == 401
        assert resp3.data['detail'] == "认证令牌无效。"

    def test_multilogin_logout(self):  # 多次登录 登录了就带token 第二次登录返回已登录
        init_superuser()
        resp = self.client.post('/api/auth/login',
                                {"username": "root", "password": "12345678"},
                                format='json')
        assert resp.status_code == 200
        assert len(resp.data['expiry']) > 0
        assert len(resp.data['token']) > 0
        authorization = "Token " + resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.post('/api/auth/login',
                                 {"username": "root", "password": "12345678"},
                                 format='json')
        assert resp2.status_code == 401
        assert resp2.data['detail'] == '你已经登陆过了'
        resp3 = self.client.post('/api/auth/logout')
        assert resp3.status_code == 204
        resp4 = self.client.post('/api/user/profile')
        assert resp4.status_code == 401
        assert resp4.data['detail'] == "认证令牌无效。"

    def test_multilogin_multitoken_multilogout(self):# 多次登录 不带token 每个独立
        init_superuser()
        authorization = []
        for i in range(11):
            resp = self.client.post('/api/auth/login',
                                    {"username": "root", "password": "12345678"},
                                    format='json')
            assert resp.status_code == 200
            assert len(resp.data['expiry']) > 0
            assert len(resp.data['token']) > 0
            authorization.append("Token " + resp.data['token'])
        for i in range(0, 10):
            self.client.credentials(HTTP_AUTHORIZATION=authorization[i])
            resp2 = self.client.get('/api/user/profile')
            assert resp2.status_code == 200
            self.assertEqual(resp2.data, {'status': 'ok', 'user': {'username': 'root', 'email': 'root@example.com'}})
        for i in range(0, 10):
            self.client.credentials(HTTP_AUTHORIZATION=authorization[i])
            resp3 = self.client.post('/api/auth/logout')
            assert resp3.status_code == 204

