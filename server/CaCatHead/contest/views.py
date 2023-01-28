from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from CaCatHead.contest.models import Contest, ContestRegistration, ContestSettings
from CaCatHead.contest.serializers import CreateContestPayloadSerializer, ContestSerializer, \
    EditContestPayloadSerializer, ContestContentSerializer, ContestRegistrationSerializer, \
    UserRegisterPayloadSerializer, ContestStandingSerializer, RatingLogSerializer
from CaCatHead.contest.services.contest import make_contest, edit_contest_payload
from CaCatHead.contest.services.rating import clear_contest_rating, refresh_contest_rating, get_contest_rating_logs
from CaCatHead.contest.services.registration import single_user_register, make_single_user_team
from CaCatHead.contest.services.submit import user_submit_problem, rejudge_submission, prepare_contest_problems
from CaCatHead.core.constants import Verdict
from CaCatHead.core.decorators import func_validate_request, SubmitRateThrottle
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.permission.constants import ContestPermissions
from CaCatHead.submission.models import ContestSubmission
from CaCatHead.submission.serializers import ContestSubmissionSerializer, FullContestSubmissionSerializer, \
    SubmitCodePayload, NoDetailContestSubmissionSerializer
from CaCatHead.utils import make_response, check_username_format


@api_view()
@cache_page(5)
@vary_on_headers("Authorization", )
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
                if contest.is_ended():
                    # 比赛已经结束
                    return contest
                elif ContestRegistration.objects.filter_register_user(contest).filter(id=user.id).count() > 0:
                    # 比赛正在进行
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
@cache_page(5)
@vary_on_headers("Authorization", )
def get_contest_public(request: Request, contest_id: int):
    contest = Contest.objects.filter_user_public(user=request.user, permission=ContestPermissions.ReadContest,
                                                 id=contest_id).first()
    if contest is None:
        raise NotFound(detail='比赛未找到')
    registration = ContestRegistration.objects.get_registration(contest=contest, user=request.user)
    return make_response(contest=ContestSerializer(contest).data,
                         registration=ContestRegistrationSerializer(registration).data)


@api_view()
@cache_page(5)
@vary_on_headers("Authorization", )
def get_contest(request: Request, contest_id: int):
    contest = check_read_contest(user=request.user, contest_id=contest_id)
    registration = ContestRegistration.objects.get_registration(contest=contest, user=request.user)

    user: User = request.user
    if user.is_authenticated:
        teams = [make_single_user_team(request.user).id]
        if registration is not None:
            teams.append(registration.team.id)
        submissions = ContestSubmission.objects.filter(repository=contest.problem_repository, owner__in=teams)
        solved = {}
        for r in submissions.values_list('problem__display_id', 'verdict'):
            pid = r[0]
            verdict = r[1]
            if pid in solved and solved[pid]:
                continue
            if verdict == Verdict.Accepted:
                solved[pid] = True
            elif verdict in [Verdict.Accepted, Verdict.WrongAnswer, Verdict.TimeLimitExceeded,
                             Verdict.IdlenessLimitExceeded,
                             Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]:
                solved[pid] = False
    else:
        solved = {}

    extra_info = None
    if contest.has_admin_permission(request.user):
        extra_info = contest.extra_info

    return make_response(contest=ContestContentSerializer(contest).data,
                         solved=solved,
                         registration=ContestRegistrationSerializer(registration).data,
                         is_admin=contest.has_admin_permission(request.user),
                         extra_info=extra_info)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
@func_validate_request(UserRegisterPayloadSerializer)
def user_register_contest(request: Request, contest_id: int):
    # 用户有注册比赛的权限
    contest = check_register_contest(user=request.user, contest_id=contest_id)
    # 比赛结束后，无法注册
    if timezone.now() > contest.end_time:
        raise BadRequest(detail='比赛已结束')
    # 检查比赛邀请码是否输入正确
    if contest.password is not None and len(contest.password) > 0:
        if 'password' in request.data:
            password = request.data['password']
            if password != contest.password:
                raise BadRequest(detail='比赛邀请码错误')
        else:
            raise BadRequest(detail='请填写比赛邀请码')
    # TODO: 检查用户是否已经注册该比赛
    name = request.data['name']
    if not check_username_format(name):
        raise BadRequest(detail="队伍名格式错误")
    registration = single_user_register(user=request.user, contest=contest,
                                        name=request.data['name'],
                                        extra_info=request.data['extra_info'])
    return make_response(registration=ContestRegistrationSerializer(registration).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_unregister_contest(request: Request, contest_id: int):
    contest = check_register_contest(user=request.user, contest_id=contest_id)
    registration = ContestRegistration.objects.get_registration(contest, request.user)

    # 比赛管理员可以取消注册
    if contest.has_admin_permission(request.user):
        registration.delete()
        return make_response()

    # 比赛开始后，无法取消注册
    if timezone.now() >= contest.start_time:
        raise BadRequest(detail='比赛已开始')

    # 只有队长可以取消注册
    if registration.team.owner == request.user:
        registration.delete()
        return make_response()
    else:
        raise BadRequest(detail='只有队伍的队长可以取消比赛注册')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([SubmitRateThrottle])
@func_validate_request(SubmitCodePayload)
def user_submit_code(request: Request, contest_id: int, problem_id: int):
    contest = check_read_contest(request.user, contest_id)
    problem = contest.get_problem(problem_id)
    if problem is None:
        raise NotFound(f'比赛 {contest.title} 没有题目 {problem_id}')
    contest_submission = user_submit_problem(request.user, contest, problem,
                                             code=request.data['code'], language=request.data['language'])
    return make_response(submission=ContestSubmissionSerializer(contest_submission).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([SubmitRateThrottle])
@func_validate_request(SubmitCodePayload)
def prepare_problem(request: Request, contest_id: int, problem_id: int):
    contest = check_read_contest(request.user, contest_id)
    problem = contest.get_problem(problem_id)
    if problem is None:
        raise NotFound(f'比赛 {contest.title} 没有题目 {problem_id}')
    if contest.has_admin_permission(request.user):
        prepare_contest_problems(request.user, contest, problem, code=request.data['code'],
                                 language=request.data['language'])
        return make_response()
    else:
        raise PermissionDenied(detail='你无权进行此操作')


@api_view()
@permission_classes([IsAuthenticated])
@cache_page(1)
@vary_on_headers("Authorization", )
def user_list_own_submissions(request: Request, contest_id: int):
    contest = check_read_contest(request.user, contest_id)
    teams = [make_single_user_team(request.user).id]
    registration = ContestRegistration.objects.get_registration(contest, request.user)
    if registration is not None:
        teams.append(registration.team.id)
    submissions = ContestSubmission.objects.filter(repository=contest.problem_repository, owner__in=teams)

    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 30))
    paginator = Paginator(submissions, page_size)
    return make_response(count=paginator.count, page=page, page_size=page_size, num_pages=paginator.num_pages,
                         submissions=ContestSubmissionSerializer(paginator.page(page).object_list, many=True).data)


@api_view()
@cache_page(5)
@vary_on_headers("Authorization", )
def user_view_all_submissions(request: Request, contest_id: int):
    contest = check_read_contest(request.user, contest_id)
    submissions = ContestSubmission.objects.filter(repository=contest.problem_repository)

    problem_id = request.query_params.get('problem', None)
    if problem_id is not None and len(problem_id) > 0:
        problem_id = int(problem_id)
        problem = contest.get_problem(problem_id)
        submissions = submissions.filter(problem__display_id=problem.display_id)

    verdict = request.query_params.get('verdict', None)
    if verdict is not None and len(verdict) > 0:
        submissions = submissions.filter(verdict=verdict)

    def get_response():
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 30))
        paginator = Paginator(submissions, page_size)
        return make_response(count=paginator.count, page=page, page_size=page_size, num_pages=paginator.num_pages,
                             submissions=ContestSubmissionSerializer(paginator.page(page).object_list, many=True).data)

    if contest.has_admin_permission(request.user):
        # 管理员用户，比赛所有者，用户自己
        return get_response()
    else:
        if contest.is_ended():
            # 比赛已经结束
            if contest.enable_settings(ContestSettings.view_submissions_after_contest):
                return get_response()
            else:
                # 没有权限访问该提交
                raise NotFound(detail='没有权限访问该提交')
        else:
            # 比赛尚未结束，无法查看其他提交
            raise NotFound(detail='比赛尚未结束，无法查看其他提交')


@api_view()
def user_view_submission(request: Request, contest_id: int, submission_id: int):
    contest = check_read_contest(request.user, contest_id)
    submission = ContestSubmission.objects.filter(repository=contest.problem_repository, id=submission_id).first()

    if submission is None:
        raise NotFound('提交未找到')
    elif contest.has_admin_permission(request.user):
        # 管理员用户，比赛所有者
        return make_response(submission=FullContestSubmissionSerializer(submission).data)
    elif submission.has_user(request.user):
        # 用户自己
        if contest.is_ended() and contest.enable_settings(ContestSettings.view_submission_checker_info):
            # 比赛结束，且打开 Checker info 才能查看 checker info
            return make_response(submission=FullContestSubmissionSerializer(submission).data)
        else:
            # 不能查看 Checker Info
            return make_response(submission=NoDetailContestSubmissionSerializer(submission).data)
    else:
        if contest.is_ended():
            # 比赛已经结束
            if contest.enable_settings(ContestSettings.view_submissions_after_contest):
                if contest.enable_settings(ContestSettings.view_submission_checker_info):
                    return make_response(submission=FullContestSubmissionSerializer(submission).data)
                else:
                    return make_response(submission=NoDetailContestSubmissionSerializer(submission).data)
            else:
                # 没有权限访问该提交
                raise NotFound(detail='没有权限访问该提交')
        else:
            # 比赛尚未结束，无法查看其他提交
            raise NotFound(detail='比赛尚未结束，无法查看其他提交')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([SubmitRateThrottle])
def rejudge_contest_submission(request: Request, contest_id: int, submission_id: int):
    contest = check_read_contest(request.user, contest_id)
    submission = ContestSubmission.objects.filter(repository=contest.problem_repository, id=submission_id).first()
    if contest.has_admin_permission(request.user):
        submission = rejudge_submission(contest, submission)
        return make_response(submission=FullContestSubmissionSerializer(submission).data)
    else:
        raise PermissionDenied(detail='你无权进行重测比赛提交操作')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([SubmitRateThrottle])
def delete_contest_submission(request: Request, contest_id: int, submission_id: int):
    contest = check_read_contest(request.user, contest_id)
    submission = ContestSubmission.objects.filter(repository=contest.problem_repository, id=submission_id).first()
    if contest.has_admin_permission(request.user):
        submission.delete()
        return make_response()
    else:
        raise PermissionDenied(detail='你无权进行删除比赛提交操作')


@api_view()
@cache_page(5)
@vary_on_headers("Authorization", )
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
            raise BadRequest(detail='您无权访问比赛榜单')
    elif contest.is_ended():
        # 比赛结束，可以查看榜单
        return response
    else:
        raise BadRequest(detail='您无权访问比赛榜单')


class RatingView(APIView):
    """
    比赛 Rating
    """
    permission_classes = [IsAdminUser]

    def get(self, request: Request, contest_id: int):
        contest = check_read_contest(request.user, contest_id)
        logs = get_contest_rating_logs(contest)
        return make_response(logs=RatingLogSerializer(logs, many=True).data)

    def post(self, request: Request, contest_id: int):
        contest = check_read_contest(request.user, contest_id)

        if contest.has_admin_permission(request.user):
            if contest.is_ended():
                refresh_contest_rating(contest)
                return make_response()
            else:
                raise BadRequest(detail='比赛还未结束')
        else:
            raise BadRequest(detail='您无权访问比赛 Rating')

    def delete(self, request: Request, contest_id: int):
        contest = check_read_contest(request.user, contest_id)
        if contest.has_admin_permission(request.user):
            if contest.is_ended():
                clear_contest_rating(contest)
                return make_response()
            else:
                raise BadRequest(detail='比赛还未结束')
        else:
            raise BadRequest(detail='您无权访问比赛 Rating')
