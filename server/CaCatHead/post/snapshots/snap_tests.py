# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot

snapshots = Snapshot()

snapshots['PostManagerTests::test_query_user_group_read_posts 1'] = GenericRepr('<QuerySet [<Post: 1. 系统公告>]>')

snapshots['PostManagerTests::test_query_user_group_read_posts 2'] = GenericRepr(
    '<QuerySet [<Post: 1. 系统公告>, <Post: 2. 公告测试>]>')

snapshots['PostManagerTests::test_query_user_public_posts 1'] = GenericRepr('<QuerySet [<Post: 1. 系统公告>]>')

snapshots[
    'PostViewTests::test_guest_view_list_posts 1'] = b'{"status":"ok","posts":[{"id":1,"owner":{"id":1,"username":"cacathead","nickname":"cacathead","rating":null,"rank":"newbie"},"created":"2022-10-27T02:20:03.089000+08:00","updated":"2022-10-27T02:20:03.089000+08:00","sort_time":"2022-10-27T02:20:03.089000+08:00","title":"\xe7\xb3\xbb\xe7\xbb\x9f\xe5\x85\xac\xe5\x91\x8a","is_public":true}]}'

snapshots[
    'PostViewTests::test_public_view_list_posts 1'] = b'{"status":"ok","posts":[{"id":1,"owner":{"id":1,"username":"cacathead","nickname":"cacathead","rating":null,"rank":"newbie"},"content":"\xe4\xbd\xa0\xe5\xa5\xbd\xef\xbc\x81","created":"2022-10-27T02:20:03.089000+08:00","updated":"2022-10-27T02:20:03.089000+08:00","sort_time":"2022-10-27T02:20:03.089000+08:00","title":"\xe7\xb3\xbb\xe7\xbb\x9f\xe5\x85\xac\xe5\x91\x8a","is_public":true,"is_home":true}]}'
