from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView


@api_view()
def hello_world(_request):
    return Response({"message": "Hello, world!"})


@api_view()
@authentication_classes([TokenAuthentication])
def current_user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    if user.is_authenticated:
        return Response({"status": "ok", "user": {"username": user.username, "email": user.email}})
    else:
        raise NotAuthenticated()


@api_view(['POST'])
def user_register(_request):
    """
    Register a new user
    """
    return Response({"status": "ok"})


class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

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
