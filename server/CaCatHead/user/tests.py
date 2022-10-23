from django.test import TestCase
from rest_framework.test import APIClient


class UserAuthTests(TestCase):
    client = APIClient()

    def test_hello_world(self):
        resp = self.client.get('/api/hello/')
        assert resp.data['message'] == 'Hello, world!'
