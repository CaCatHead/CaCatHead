from django.conf import settings
from django.core.cache import caches
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from CaCatHead.user.models import UserToken


def set_user_token(token: str, user_id: int):
    cache = caches['auth']
    cache.set(token, str(user_id), settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())


def delete_user_token(token: str):
    cache = caches['auth']
    cache.delete(token)
    UserToken.objects.filter(key=token).delete()


def get_user_token(token: str):
    cache = caches['auth']
    return cache.get(token)


class JWTCookieAuthentication(JWTAuthentication):
    """
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).
    """

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise PermissionDenied(f'CSRF Failed: {reason}')

    def authenticate(self, request: Request):
        cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if raw_token is not None and settings.REST_AUTH['JWT_AUTH_COOKIE_USE_CSRF']:
                    self.enforce_csrf(request)
            else:
                return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            if get_user_token(validated_token) is not None:
                if request.path.startswith('/api/auth/logout'):
                    delete_user_token(raw_token)
                return self.get_user(validated_token), validated_token
            else:
                raise AuthenticationFailed('认证令牌无效。')
        except InvalidToken:
            delete_user_token(raw_token)
            return None
