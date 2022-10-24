from django.contrib.auth.models import User

from .models import UserInfo, StudentInfo


def register_student_user(username: str, email: str, password: str):
    """
    Create and save a student User
    """
    email = User.objects.normalize_email(email)
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
