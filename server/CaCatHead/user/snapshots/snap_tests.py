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

snapshots['UserAuthTests::test_flow 2'] = {
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

snapshots['UserAuthTests::test_login 1'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 1'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 10'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 2'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 3'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 4'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 5'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 6'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 7'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 8'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_multi_login_logoutall 9'] = {
    'email': 'root@example.com',
    'id': 1,
    'nickname': 'cacathead',
    'permissions': {
        'add_contest': True,
        'add_post': True,
        'is_staff': True,
        'is_superuser': True,
        'polygon': True
    },
    'rank': 'rainbow',
    'rating': None,
    'username': 'cacathead'
}

snapshots['UserAuthTests::test_password_error 1'] = '用户名或者密码错误'

snapshots['UserAuthTests::test_username_error 1'] = '用户名或者密码错误'

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
