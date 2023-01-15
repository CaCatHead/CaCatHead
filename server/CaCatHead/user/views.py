from datetime import datetime

import gmpy2
import pytz
from django.contrib.auth import authenticate, login
from django.utils import timezone
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from CaCatHead.core.decorators import func_validate_request, class_validate_request, RegisterRateThrottle, \
    LoginRateThrottle
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.user.serializers import LoginPayloadSerializer, RegisterPayloadSerializer, FullUserSerializer
from CaCatHead.user.services import register_student_user
from CaCatHead.utils import make_response


@api_view()
def ping(_request: Request):
    return make_response(message="Hello, world!")


@api_view()
def sync_timestamp(request: Request):
    client = datetime.utcfromtimestamp(int(request.query_params.get('timestamp'))).replace(tzinfo=pytz.UTC)
    server = timezone.now()
    return make_response(diff=round((server - client).total_seconds() * 1000),
                         timestamp=round(server.timestamp() * 1000))


@api_view()
def is_prime(request: Request, text: str):
    if len(text) > 1000:
        raise BadRequest(detail='Your number is too big')
    try:
        n = int(text)
        return make_response(prime=gmpy2.is_prime(n))
    except ValueError:
        raise BadRequest(detail='Your request is not a number')


@api_view()
@permission_classes([IsAuthenticated])
def current_user_profile(request: Request):
    """
    获取当前用户信息
    """
    user = request.user
    return make_response(user=FullUserSerializer(user).data)


@api_view(['POST'])
@throttle_classes([RegisterRateThrottle])
@func_validate_request(RegisterPayloadSerializer)
def user_register(request: Request):
    """
    注册新用户
    """
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = register_student_user(username=username, email=email, password=password)
    return make_response(user=FullUserSerializer(user).data)


class UserLoginView(KnoxLoginView):
    """
    用户登录
    """

    permission_classes = (permissions.AllowAny,)

    throttle_classes = (LoginRateThrottle,)

    @class_validate_request(LoginPayloadSerializer)
    def post(self, request: Request, _format=None):
        if request.user.is_authenticated:
            raise AuthenticationFailed('你已经登陆过了')
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return super(UserLoginView, self).post(request, format=None)
        else:
            raise AuthenticationFailed()
