import logging
from datetime import datetime

import gmpy2
import pytz
from dj_rest_auth import views as AuthViews
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.cache import cache_page
from ipware import get_client_ip
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from CaCatHead.contest.models import Contest
from CaCatHead.contest.serializers import ContestSerializer
from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY as MAIN_PROBLEM_REPOSITORY_NAME
from CaCatHead.core.decorators import func_validate_request, class_validate_request, RegisterRateThrottle, \
    LoginRateThrottle
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.permission.constants import ProblemRepositoryPermissions
from CaCatHead.post.models import Post
from CaCatHead.post.serializers import PostContentSerializer, PostSerializer
from CaCatHead.problem.models import ProblemRepository
from CaCatHead.problem.serializers import ProblemRepositorySerializer
from CaCatHead.problem.views import get_main_problem_repo
from CaCatHead.user.models import UserToken
from CaCatHead.user.serializers import LoginPayloadSerializer, RegisterPayloadSerializer, FullUserSerializer, \
    UserPublicSerializer
from CaCatHead.user.services import register_student_user
from CaCatHead.utils import make_response, check_username_format

logger = logging.getLogger(__name__)


@api_view()
def ping(_request: Request):
    return make_response(message="Hello, world!")


@api_view()
def sync_timestamp(request: Request):
    client = datetime.utcfromtimestamp(int(request.query_params.get('timestamp'))).replace(tzinfo=pytz.UTC)
    server = timezone.now()
    return make_response(diff=round((server - client).total_seconds() * 1000),
                         timestamp=round(server.timestamp() * 1000))


@api_view()
def is_prime(request: Request, text: str):
    if len(text) > 1000:
        raise BadRequest(detail='Your number is too big')
    try:
        n = int(text)
        return make_response(prime=gmpy2.is_prime(n))
    except ValueError:
        raise BadRequest(detail='Your request is not a number')
    except Exception:
        raise BadRequest(detail='Something went wrong')


@api_view()
@cache_page(60)
def get_home_info(request: Request):
    posts = Post.objects.filter_public().filter(is_home=True).all()[:10]
    recent_posts = Post.objects.filter_public().all()[:20]
    recent_contests = Contest.objects.filter_public().all()[:5]
    top_users = User.objects.filter(userinfo__rating__isnull=False).order_by('-userinfo__rating').all()[:5]
    return make_response(commit_sha=settings.COMMIT_SHA,
                         posts=PostContentSerializer(posts, many=True).data,
                         recent_posts=PostSerializer(recent_posts, many=True).data,
                         recent_contests=ContestSerializer(recent_contests, many=True).data,
                         top_users=UserPublicSerializer(top_users, many=True).data)


@api_view()
@permission_classes([IsAuthenticated])
def current_user_profile(request: Request):
    """
    获取当前用户信息
    """
    user = request.user
    main_repo = get_main_problem_repo()
    if main_repo is None:
        main_repo = ProblemRepository.objects.get(name=MAIN_PROBLEM_REPOSITORY_NAME)
    repos = ProblemRepository.objects.filter_user_public(user=request.user,
                                                         permission=ProblemRepositoryPermissions.ListProblems).filter(
        ~Q(id=main_repo.id)).filter(is_contest=False)
    return make_response(user=FullUserSerializer(user).data,
                         repos=ProblemRepositorySerializer(repos, many=True).data)


@api_view()
def get_user_info(request: Request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        return make_response(user=UserPublicSerializer(user).data)
    else:
        raise NotFound(detail=f'用户 {username} 未找到')


@api_view(['POST'])
@throttle_classes([RegisterRateThrottle])
@func_validate_request(RegisterPayloadSerializer)
def user_register(request: Request):
    """
    注册新用户
    """
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    if not check_username_format(username):
        raise BadRequest(detail="用户名格式错误")
    user = register_student_user(username=username, email=email, password=password)
    return make_response(user=FullUserSerializer(user).data)


class UserLoginView(AuthViews.LoginView):
    """
    用户登录
    """

    permission_classes = (permissions.AllowAny,)

    throttle_classes = (LoginRateThrottle,)

    @class_validate_request(LoginPayloadSerializer)
    def post(self, request: Request, _format=None):
        if request.user.is_authenticated:
            raise AuthenticationFailed('你已经登陆过了')
        if not check_username_format(request.data['username']):
            raise BadRequest(detail="用户名格式错误")

        try:
            resp = super(UserLoginView, self).post(request)
            client_ip, is_routable = get_client_ip(request)
            if client_ip is not None:
                user_agent = request.headers.get('User-Agent')
                if settings.IS_TEST:
                    user_agent = 'test'
                if user_agent is not None and len(user_agent) > 0:
                    user_token = UserToken(
                        key=resp.data['access_token'],
                        login_ip=client_ip,
                        expiry_time=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        user_agent=user_agent,
                        user_id=resp.data['user']['id'],
                    )
                    user_token.save()
                    return resp
                else:
                    raise AuthenticationFailed("UA 非法")
            else:
                raise AuthenticationFailed("IP 非法")
        except ValidationError as validation:
            if 'non_field_errors' in validation.detail and isinstance(validation.detail['non_field_errors'], list):
                errors = validation.detail['non_field_errors']
                if len(errors) > 0 and str(errors[0]) == '无法使用提供的认证信息登录。':
                    raise AuthenticationFailed(detail='用户名或者密码错误')
            logger.error(validation)
            raise AuthenticationFailed(detail=str(validation.detail))


class UserLogoutView(AuthViews.LogoutView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        return super(UserLogoutView, self).post(request)
