# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['UserAuthTests::test_hello_world 1'] = {
    'message': 'Hello, world!',
    'status': 'ok'
}
