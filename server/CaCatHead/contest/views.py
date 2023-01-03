from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from CaCatHead.contest.models import Contest
from CaCatHead.contest.serializers import CreateContestPayloadSerializer, ContestSerializer, \
    EditContestPayloadSerializer, ContestContentSerializer
from CaCatHead.contest.services import make_contest, edit_contest_payload
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
    return make_response(contest=ContestContentSerializer(contest).data)


def check_read_contest(user: User, contest_id: int):
    contest = Contest.objects.filter_user_permission(user=user, permission=ContestPermissions.ReadContest,
                                                     id=contest_id).first()
    if contest is not None:
        return contest
    else:
        raise NotFound(detail='比赛未找到或权限不足')


def check_contest(user: User, contest_id: int, permission: str):
    contest = Contest.objects.filter_user_permission(user=user, permission=permission, id=contest_id).first()
    if contest is not None:
        return contest
    else:
        raise NotFound(detail='比赛未找到或权限不足')


@api_view()
def get_contest(request: Request, contest_id: int):
    contest = check_read_contest(user=request.user, contest_id=contest_id)
    return make_response(contest=ContestContentSerializer(contest).data)


@api_view(['POST'])
@func_validate_request(EditContestPayloadSerializer)
def edit_contest(request: Request, contest_id: int):
    contest = check_contest(user=request.user, contest_id=contest_id, permission=ContestPermissions.EditContest)
    contest = edit_contest_payload(request.user, contest, request.data)
    return make_response(contest=ContestContentSerializer(contest).data)
