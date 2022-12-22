# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UserAuthTests::test_flow 1'] = {
    'email': 'world@example.com',
    'id': 2,
    'nickname': 'world',
    'polygon': False,
    'username': 'world'
}

snapshots['UserAuthTests::test_flow 2'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 2,
        'nickname': 'world',
        'polygon': False,
        'username': 'world'
    }
}

snapshots['UserAuthTests::test_hello_world 1'] = {
    'message': 'Hello, world!',
    'status': 'ok'
}

snapshots['UserAuthTests::test_login 1'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 1'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 10'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 2'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 3'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 4'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 5'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 6'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 7'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 8'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 9'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'polygon': True,
        'username': 'root'
    }
}

snapshots['UserRegisterTests::test_register_ok_same_email 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 2,
        'nickname': 'world',
        'polygon': False,
        'username': 'world'
    }
}
