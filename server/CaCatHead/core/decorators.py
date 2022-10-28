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
