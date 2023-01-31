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
                         u"\U000024C2-\U0001F251"
                         u"\U0001f926-\U0001f937"
                         u"\U00010000-\U0010ffff"
                         u"\u2640-\u2642"
                         u"\u2600-\u2b55"
                         u"\u200d\u23cf\u23e9"
                         u"\u231a\ufe0f\u3030"
                         u"]*$", flags=re.UNICODE)

VIEW_RE = re.compile(r"^[\w\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]$")


def check_username_format(s: str) -> bool:
    def is_ch(c: str):
        return VIEW_RE.match(c) is not None

    ok = False
    for c in s:
        if c == 'ㅤ':
            return False
        elif c.isalnum() or is_ch(c):
            ok = True
        elif USERNAME_RE.match(c) is None:
            return False
    return ok
