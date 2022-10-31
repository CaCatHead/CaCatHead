from rest_framework.response import Response


def make_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'ok', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)


def make_error_response(status=None, headers=None, exception=None, **kwargs):
    return Response(data={'status': 'error', **kwargs}, status=status, headers=headers, exception=exception,
                    content_type=None, template_name=None)
