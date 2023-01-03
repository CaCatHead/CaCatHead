from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from CaCatHead.contest.serializers import CreateContestPayloadSerializer
from CaCatHead.core.decorators import func_validate_request
from CaCatHead.utils import make_response


@api_view()
def list_contests(request: Request):
    return make_response(contests=[])


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@permission_required('contest.add_contest', raise_exception=True)
@func_validate_request(CreateContestPayloadSerializer)
def create_contest(request: Request):
    """
    创建比赛
    """
    return make_response(contest=None)


@api_view(['POST'])
def edit_contest(request: Request):
    return make_response()
