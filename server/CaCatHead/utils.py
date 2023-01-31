import re

from rest_framework.response import Response


def make_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'ok', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)


def make_error_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'error', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)


USERNAME_RE = re.compile(r"^[\w"
                         u"\u4e00-\u9fa5"
                         u"\u3040-\u309f\u30a0-\u30ff"
                         u"\U0001F600-\U0001F64F"
                         u"\U0001F300-\U0001F5FF"
                         u"\U0001F680-\U0001F6FF"
                         u"\U0001F1E0-\U0001F1FF"
                         u"\U00002702-\U000027B0"
                         u"\U00002702-\U000027B0"
                         u"\U000024C2-\U0001F251"
                         u"\U0001f926-\U0001f937"
                         u"\U00010000-\U0010ffff"
                         u"\u2640-\u2642"
                         u"\u2600-\u2B55"
                         u"\u200d"
                         u"\u23cf"
                         u"\u23e9"
                         u"\u231a"
                         u"\ufe0f"
                         u"\u3030"
                         r"]+$", flags=re.UNICODE)


def check_username_format(s: str) -> bool:
    return USERNAME_RE.match(s) is not None
