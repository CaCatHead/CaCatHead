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
        # 随机搞一个token访问/api/user/profile 返回401
        authorization = resp.data['token']
        reversed(authorization)
        authorization = "Token " + authorization + "c"
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        resp2 = self.client.get('/api/user/profile')
        self.assertEqual(resp2.status_code, 401)

    def test_tokenError_authentication_failed(self):
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

