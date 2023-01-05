from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, APIException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from CaCatHead.contest.models import Contest, ContestRegistration, ContestSettings
from CaCatHead.contest.serializers import CreateContestPayloadSerializer, ContestSerializer, \
    EditContestPayloadSerializer, ContestContentSerializer, ContestRegistrationSerializer, \
    UserRegisterPayloadSerializer, ContestStandingSerializer
from CaCatHead.contest.services.contest import make_contest, edit_contest_payload
from CaCatHead.contest.services.registration import single_user_register, make_single_user_team
from CaCatHead.contest.services.submit import user_submit_problem
from CaCatHead.core.decorators import func_validate_request
from CaCatHead.permission.constants import ContestPermissions
from CaCatHead.problem.serializers import SubmitCodePayload
from CaCatHead.submission.models import ContestSubmission
from CaCatHead.submission.serializers import ContestSubmissionSerializer, FullContestSubmissionSerializer
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
    contest = Contest.objects.filter_user_public(user=user,
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
    contest = Contest.objects.filter_user_public(user=request.user, permission=ContestPermissions.ReadContest,
                                                 id=contest_id).first()
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
    # 检查比赛邀请码是否输入正确
    if contest.password is not None and len(contest.password) > 0:
        if 'password' in request.data:
            password = request.data['password']
            if password != contest.password:
                raise APIException(detail='比赛邀请码错误', code=400)
        else:
            raise APIException(detail='请填写比赛邀请码', code=400)
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
    return make_response(submission=ContestSubmissionSerializer(contest_submission).data)


@api_view()
def user_list_own_submissions(request: Request, contest_id: int):
    contest = check_read_contest(request.user, contest_id)
    teams = [make_single_user_team(request.user).id]
    registration = ContestRegistration.objects.get_registration(contest, request.user)
    if registration is not None:
        teams.append(registration.team.id)
    submissions = ContestSubmission.objects.filter(repository=contest.problem_repository, owner__in=teams)
    return make_response(submissions=ContestSubmissionSerializer(submissions, many=True).data)


@api_view()
def user_view_submission(request: Request, contest_id: int, submission_id: int):
    contest = check_read_contest(request.user, contest_id)
    submission = ContestSubmission.objects.filter(repository=contest.problem_repository, id=submission_id).first()

    if submission is None:
        raise NotFound('提交未找到')
    elif contest.has_admin_permission(request.user) or submission.has_user(request.user):
        # 管理员用户，比赛所有者，用户自己
        return make_response(submission=FullContestSubmissionSerializer(submission).data)
    else:
        if contest.is_ended():
            # 比赛已经结束
            if contest.enable_settings(ContestSettings.view_submissions_after_contest):
                return make_response(submission=FullContestSubmissionSerializer(submission).data)
            else:
                # 没有权限访问该提交
                raise NotFound(detail='没有权限访问该提交')
        else:
            # 比赛尚未结束，无法查看其他提交
            raise NotFound(detail='比赛尚未结束，无法查看其他提交')


@api_view()
def user_view_standings(request: Request, contest_id: int):
    contest = check_read_contest(request.user, contest_id)
    registrations = ContestRegistration.objects.filter(contest=contest)
    response = make_response(registrations=ContestStandingSerializer(registrations, many=True).data)

    if contest.has_admin_permission(request.user):
        # 管理员可以查看榜单
        return response
    elif contest.is_running():
        # 比赛进行中，必须打开设置才能查看榜单
        if contest.enable_settings(ContestSettings.view_standings):
            return response
        else:
            raise APIException(detail='您无权访问比赛榜单', code=400)
    elif contest.is_ended():
        # 比赛结束，可以查看榜单
        return response
    else:
        raise APIException(detail='您无权访问比赛榜单', code=400)
