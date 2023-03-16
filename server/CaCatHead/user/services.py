import logging

from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from CaCatHead.core.constants import GENERAL_USER_GROUP
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.user.models import UserInfo, StudentInfo

logger = logging.getLogger(__name__)


def get_general_user_group() -> Group:
    return Group.objects.filter(name=GENERAL_USER_GROUP).first()


def register_student_user(username: str, email: str, password: str, nickname: str = None):
    """
    Create and save a student User
    """
    email = User.objects.normalize_email(email)
    user = None
    user_info = None
    student_info = None
    try:
        user = User(username=username,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    is_superuser=False,
                    )
        user.set_password(password)
        user.save()
        if nickname is None:
            nickname = username
        user_info = UserInfo(user=user, nickname=nickname, is_teacher=False)
        user_info.save()
        student_info = StudentInfo(user=user, student_name=nickname)
        student_info.save()

        # 非超级用户都加入默认用户组
        user.groups.add(get_general_user_group())

        # 创建代表用户自己的团队，用于个人参加比赛
        # make_single_user_team(user)

        return user
    except IntegrityError as error:
        logger.error(error)

        message = '未知的数据库错误'
        if type(error.args) == tuple and len(error.args) > 0:
            if error.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = f'用户名 {username} 已经被注册'
            elif error.args[0] == 'UNIQUE constraint failed: user_info.nickname':
                message = f'用户名 {username} 已经被注册'

        # 清空中间状态生成的用户
        if user_info is not None:
            user_info.delete()
        if student_info is not None:
            student_info.delete()
        if user is not None:
            user.delete()

        raise BadRequest(detail=message)


def register_superuser(username: str, email: str, password: str):
    """
    Create and save a student User
    """
    email = User.objects.normalize_email(email)
    try:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.save()
        user_info = UserInfo(user=user, nickname=username, rank='rainbow', is_teacher=False)
        user_info.save()
        student_info = StudentInfo(user=user, student_name=username)
        student_info.save()

        # 创建代表用户自己的团队，用于个人参加比赛
        # make_single_user_team(user)

        return user
    except IntegrityError as error:
        logger.error(error)
        message = '未知的数据库错误'
        if type(error.args) == tuple and len(error.args) > 0:
            if error.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = f'用户名 {username} 已经被注册'
        raise BadRequest(detail=message)


def register_admin_user(username: str, email: str, password: str):
    """
    Create and save an admin User
    """
    user = register_student_user(username, email, password)
    user.is_staff = True
    user.save()
    return user
