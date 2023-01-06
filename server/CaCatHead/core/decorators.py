from rest_framework.permissions import BasePermission
from rest_framework.throttling import UserRateThrottle

from CaCatHead.core.constants import Permissions


def class_validate_request(serializer_class):
    """
    Validate request data, receive a subclass of serializers.Serializer
    """

    def decorator(func):
        def wrapped_view(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return func(self, request, *args, **kwargs)

        return wrapped_view

    return decorator


def func_validate_request(serializer_class):
    """
    Validate request data, receive a subclass of serializers.Serializer
    """

    def decorator(func):
        def wrapped_view(request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return func(request, *args, **kwargs)

        return wrapped_view

    return decorator


class HasPolygonPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return True
            return user.has_perm(Permissions.POLYGON)
        else:
            return False


class SubmitRateThrottle(UserRateThrottle):
    rate = '12/minute'
