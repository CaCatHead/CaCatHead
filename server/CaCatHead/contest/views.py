from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, APIException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from CaCatHead.contest.models import Contest, ContestRegistration
from CaCatHead.contest.serializers import CreateContestPayloadSerializer, ContestSerializer, \
    EditContestPayloadSerializer, ContestContentSerializer, ContestRegistrationSerializer, \
    UserRegisterPayloadSerializer
from CaCatHead.contest.services.contest import make_contest, edit_contest_payload
from CaCatHead.contest.services.registration import single_user_register
from CaCatHead.contest.services.submit import user_submit_problem
from CaCatHead.core.decorators import func_validate_request
from CaCatHead.permission.constants import ContestPermissions
from CaCatHead.problem.serializers import SubmitCodePayload
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


def check_read_contest(user: User, contest_id: int) -> Contest:
    contest = Contest.objects.filter_user_permission(user=user,
                                                     permission=ContestPermissions.ReadContest,
                                                     id=contest_id).first()
    if contest is not None:
        return contest
    else:
        contest = Contest.objects.filter_user_public(user=user, permission=ContestPermissions.ReadContest,
                                                     id=contest_id).first()
        if contest is not None:
            if contest.is_started():
                if ContestRegistration.objects.filter_register_user(contest).filter(id=user.id).count() > 0:
                    return contest
                else:
                    raise NotFound(detail='你尚未注册该比赛')
            else:
                raise NotFound(detail='比赛尚未开始')
        else:
            raise NotFound(detail='比赛未找到')


def check_register_contest(user: User, contest_id: int) -> Contest:
    contest = Contest.objects.filter_user_permission(user=user,
                                                     permission=ContestPermissions.RegisterContest,
                                                     id=contest_id).first()
    if contest is not None:
        return contest
    else:
        raise NotFound(detail='比赛未找到或权限不足')


def check_contest(user: User, contest_id: int, permission: str) -> Contest:
    contest = Contest.objects.filter_user_permission(user=user, permission=permission, id=contest_id).first()
    if contest is not None:
        return contest
    else:
        raise NotFound(detail='比赛未找到或权限不足')


@api_view()
def get_contest_public(request: Request, contest_id: int):
    contest = check_read_contest(user=request.user, contest_id=contest_id)
    registration = ContestRegistration.objects.get_registration(contest=contest, user=request.user)
    return make_response(contest=ContestSerializer(contest).data,
                         registration=ContestRegistrationSerializer(registration).data)


@api_view()
def get_contest(request: Request, contest_id: int):
    contest = check_read_contest(user=request.user, contest_id=contest_id)
    registration = ContestRegistration.objects.get_registration(contest=contest, user=request.user)
    return make_response(contest=ContestContentSerializer(contest).data,
                         registration=ContestRegistrationSerializer(registration).data)


@api_view(['POST'])
@func_validate_request(EditContestPayloadSerializer)
def edit_contest(request: Request, contest_id: int):
    contest = check_contest(user=request.user, contest_id=contest_id, permission=ContestPermissions.EditContest)
    contest = edit_contest_payload(request.user, contest, request.data)
    return make_response(contest=ContestContentSerializer(contest).data)


class ContestRegistrationView(APIView):
    """
    编辑比赛注册者列表
    """

    def get(self, request: Request, contest_id: int):
        contest = check_contest(user=request.user, contest_id=contest_id, permission=ContestPermissions.EditContest)
        registrations = ContestRegistration.objects.filter_registration(contest).all()

        return make_response(registrations=ContestRegistrationSerializer(registrations, many=True).data)

    def post(self, request: Request, contest_id: int):
        return make_response()


@api_view(['POST'])
@func_validate_request(UserRegisterPayloadSerializer)
def user_register_contest(request: Request, contest_id: int):
    # 用户有注册比赛的权限
    contest = check_register_contest(user=request.user, contest_id=contest_id)
    # 比赛尚未结束
    if timezone.now() > contest.end_time:
        raise APIException(detail='比赛已结束', code=400)
    # TODO: 检查用户是否已经注册该比赛
    registration = single_user_register(user=request.user, contest=contest,
                                        name=request.data['name'],
                                        extra_info=request.data['extra_info'])
    return make_response(registration=ContestRegistrationSerializer(registration).data)


@api_view(['POST'])
@func_validate_request(SubmitCodePayload)
def user_submit_code(request: Request, contest_id: int, problem_id: int):
    contest = check_read_contest(request.user, contest_id)
    problem = contest.get_problem(problem_id)
    if problem is None:
        raise NotFound(f'比赛 {contest.title} 没有题目 {problem_id}')
    contest_submission = user_submit_problem(request.user, contest, problem,
                                             code=request.data['code'], language=request.data['language'])
    return make_response()
