import re

from rest_framework.response import Response


def make_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'ok', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)


def make_error_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'error', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)


USERNAME_RE = re.compile(r'^[\u4e00-\u9fa5\w\U00010000-\U0010ffff]+$')


def check_username_format(s: str) -> bool:
    return USERNAME_RE.match(s) is not None
