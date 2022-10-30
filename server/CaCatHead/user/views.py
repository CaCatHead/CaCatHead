from django.contrib.auth import authenticate, login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from CaCatHead.utils import make_response
from CaCatHead.core.decorators import func_validate_request, class_validate_request
from CaCatHead.user.serializer import LoginPayloadSerializer, RegisterPayloadSerializers
from CaCatHead.user.service import register_student_user


@api_view()
def ping(_request):
    return make_response(message="Hello, world!")


@api_view()
@permission_classes([IsAuthenticated])
def current_user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    return make_response(user={"username": user.username, "email": user.email})


@api_view(['POST'])
@func_validate_request(RegisterPayloadSerializers)
def user_register(request):
    """
    Register a new user
    """
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = register_student_user(username=username, email=email, password=password)
    return make_response(user={"username": user.username, "email": user.email})


class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

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
