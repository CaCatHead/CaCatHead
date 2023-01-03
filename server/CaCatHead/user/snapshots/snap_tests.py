# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['UserAuthTests::test_flow 1'] = {
    'email': 'world@example.com',
    'id': 5,
    'nickname': 'world',
    'permissions': {
        'add_contest': False,
        'add_post': False,
        'polygon': False
    },
    'username': 'world'
}

snapshots['UserAuthTests::test_flow 2'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 5,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'polygon': False
        },
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
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 1'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 10'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 2'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 3'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 4'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 5'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 6'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 7'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 8'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 9'] = {
    'status': 'ok',
    'user': {
        'email': 'root@example.com',
        'id': 1,
        'nickname': 'root',
        'permissions': {
            'add_contest': True,
            'add_post': True,
            'polygon': True
        },
        'username': 'root'
    }
}

snapshots['UserRegisterTests::test_register 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 6,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'polygon': False
        },
        'username': 'world'
    }
}

snapshots['UserRegisterTests::test_register_error_same_username 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 7,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'polygon': False
        },
        'username': 'world'
    }
}

snapshots['UserRegisterTests::test_register_ok_same_email 1'] = {
    'status': 'ok',
    'user': {
        'email': 'world@example.com',
        'id': 9,
        'nickname': 'world',
        'permissions': {
            'add_contest': False,
            'add_post': False,
            'polygon': False
        },
        'username': 'world'
    }
}
