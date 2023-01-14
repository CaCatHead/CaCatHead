from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import UserInfo, StudentInfo
from ..core.exceptions import BadRequest


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
        return user
    except IntegrityError as error:
        message = '未知的数据库错误'
        if type(error.args) == tuple and len(error.args) > 0:
            if error.args[0] == 'UNIQUE constraint failed: auth_user.username':
                message = f'用户名 {username} 已经被注册'
        raise BadRequest(detail=message)
