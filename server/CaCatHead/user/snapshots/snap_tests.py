# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['UserAuthTests::test_flow 1'] = {
    'email': 'world@example.com',
    'id': 2,
    'nickname': 'world',
    'permissions': {
        'add_contest': False,
        'add_post': False,
        'is_staff': False,
        'is_superuser': False,
        'polygon': False
    },
    'rank': 'newbie',
    'rating': None,
    'username': 'world'
}

snapshots['UserAuthTests::test_hello_world 1'] = {
    'message': 'Hello, world!',
    'status': 'ok'
}

snapshots['UserRegisterTests::test_register 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 2,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'is_staff': False,
            'is_superuser': False,
            'polygon': False
        },
        'rank': 'newbie',
        'rating': None,
        'username': 'world'
    }
}

snapshots['UserRegisterTests::test_register_error_same_username 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 2,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'is_staff': False,
            'is_superuser': False,
            'polygon': False
        },
        'rank': 'newbie',
        'rating': None,
        'username': 'world'
    }
}

snapshots['UserRegisterTests::test_register_ok_same_email 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 2,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'is_staff': False,
            'is_superuser': False,
            'polygon': False
        },
        'rank': 'newbie',
        'rating': None,
        'username': 'world'
    }
}
