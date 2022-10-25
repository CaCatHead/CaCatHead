from rest_framework.test import APITestCase


class UserAuthTests(APITestCase):
    def test_hello_world(self):
        resp = self.client.get('/api/hello/')
        assert resp.status_code == 200
        assert resp.data['message'] == 'Hello, world!'

    def test_login(self):
        resp = self.client.post('/api/auth/login',
                                {"username": "root", "password": "12345678"},
                                format='json')
        assert resp.status_code == 200
        assert len(resp.data['expiry']) > 0
        assert len(resp.data['token']) > 0

        # TODO: send GET request to /api/user/profile to check TOKEN is valid
