from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from CaCatHead.contest.models import Contest
from CaCatHead.contest.serializers import CreateContestPayloadSerializer, ContestSerializer
from CaCatHead.contest.services import make_contest
from CaCatHead.core.decorators import func_validate_request
from CaCatHead.permission.constants import ContestPermissions
from CaCatHead.utils import make_response


@api_view()
def list_contests(request: Request):
    contests = Contest.objects.filter_user_public(user=request.user, permission=ContestPermissions.ReadContest)
    return make_response(contests=ContestSerializer(contests, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@permission_required('contest.add_contest', raise_exception=True)
@func_validate_request(CreateContestPayloadSerializer)
def create_contest(request: Request):
    """
    创建比赛
    """
    contest = make_contest(user=request.user, title=request.data['title'], type=request.data['type'])
    return make_response(contest=ContestSerializer(contest).data)


@api_view(['POST'])
def edit_contest(request: Request):
    return make_response()
