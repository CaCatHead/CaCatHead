from rest_framework.test import APITestCase
from snapshottest.django import TestCase as SnapshotTestCase


class TestCase(APITestCase, SnapshotTestCase):
    pass
