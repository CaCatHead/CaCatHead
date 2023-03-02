# Generated by Django 4.1.2 on 2022-10-30 19:02
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import migrations, models

from CaCatHead.core.constants import NJUST_ICPC_GROUP
from CaCatHead.user.models import UserInfo


def init_team_group(_apps, _schema_editor):
    """
    初始化集训队成员 Group
    """
    team_group = Group(name=NJUST_ICPC_GROUP)
    team_group.save()


def init_superuser(_apps, _schema_editor):
    """
    初始化超级用户
    """
    username = settings.CACATHEAD_ROOT_USER
    password = settings.CACATHEAD_ROOT_PASS
    email = 'root@example.com'
    user = User.objects.create_superuser(username=username, email=email, password=password)
    user_info = UserInfo(user=user, nickname=username, rank='rainbow', is_teacher=False)
    user_info.save()
    return user


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='rating',
            field=models.IntegerField(default=None, null=True, verbose_name='Rating'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='rank',
            field=models.CharField(default='newbie', max_length=32, verbose_name='Rank'),
        ),
        migrations.RunPython(init_superuser),
        migrations.RunPython(init_team_group),
    ]
