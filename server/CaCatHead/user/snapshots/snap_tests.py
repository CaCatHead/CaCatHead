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
    'username': 'world'
}

snapshots['UserAuthTests::test_flow 2'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        }
    ],
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
        'username': 'world'
    }
}

snapshots['UserAuthTests::test_hello_world 1'] = {
    'message': 'Hello, world!',
    'status': 'ok'
}

snapshots['UserAuthTests::test_login 1'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 1'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 10'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 2'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 3'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 4'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 5'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 6'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 7'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 8'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
}

snapshots['UserAuthTests::test_multi_login_logoutall 9'] = {
    'repos': [
        {
            'id': 1,
            'is_public': True,
            'name': '题库'
        },
        {
            'id': 2,
            'is_public': False,
            'name': 'C++ 基础'
        },
        {
            'id': 3,
            'is_public': False,
            'name': 'C++ 练习'
        },
        {
            'id': 4,
            'is_public': False,
            'name': 'C++ 考试'
        },
        {
            'id': 5,
            'is_public': False,
            'name': '数据结构基础'
        },
        {
            'id': 6,
            'is_public': False,
            'name': '数据结构练习'
        },
        {
            'id': 7,
            'is_public': False,
            'name': '数据结构考试'
        },
        {
            'id': 8,
            'is_public': False,
            'name': '算法基础'
        },
        {
            'id': 9,
            'is_public': False,
            'name': '算法练习'
        },
        {
            'id': 10,
            'is_public': False,
            'name': '算法考试'
        },
        {
            'id': 11,
            'is_public': False,
            'name': 'CCF'
        }
    ],
    'status': 'ok',
    'user': {
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
        'username': 'cacathead'
    }
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
        'username': 'world'
    }
}
