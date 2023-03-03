from django.contrib.auth.models import User, Group
from django.db import IntegrityError

from .models import UserInfo, StudentInfo
from ..contest.services.registration import make_single_user_team
from ..core.constants import GENERAL_USER_GROUP
from ..core.exceptions import BadRequest


def get_general_user_group() -> Group:
    return Group.objects.filter(name=GENERAL_USER_GROUP).first()


def register_student_user(username: str, email: str, password: str):
    """
    Create and save a student User
    """
    email = User.objects.normalize_email(email)
    try:
        user = User(username=username,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    is_superuser=False,
                    )
        user.set_password(password)
        user.save()
        user_info = UserInfo(user=user, nickname=username, is_teacher=False)
        user_info.save()
        student_info = StudentInfo(user=user, student_name=username)
        student_info.save()

        # 非超级用户都加入默认用户组
        user.groups.add(get_general_user_group())

        # 创建代表用户自己的团队，用于个人参加比赛
        make_single_user_team(user)

        return user
    except IntegrityError as error:
        message = '未知的数据库错误'
        if type(error.args) == tuple and len(error.args) > 0:
            if error.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = f'用户名 {username} 已经被注册'
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
        make_single_user_team(user)

        return user
    except IntegrityError as error:
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
