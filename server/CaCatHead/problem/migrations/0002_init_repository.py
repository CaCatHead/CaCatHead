from django.contrib.auth.models import User
from django.db import migrations

from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY
from CaCatHead.problem.models import ProblemRepository

REPOS = [
    '题库',
    'C++ 基础',
    'C++ 练习',
    'C++ 考试',
    '数据结构基础',
    '数据结构练习',
    '数据结构考试',
    '算法基础',
    '算法练习',
    '算法考试',
    'CCF',
]


def init_problem_repository(_apps, _schema_editor):
    """
    初始化题库
    """
    root = User.objects.filter(is_superuser=True).first()
    for repo_name in REPOS:
        repo = ProblemRepository(name=repo_name, owner=root, is_public=repo_name == REPOS[0])
        repo.save()
    main_repo = ProblemRepository(name=MAIN_PROBLEM_REPOSITORY, owner=root, is_public=False)
    main_repo.save()


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0001_initial'),
        ('user', '0002_root')
    ]

    operations = [
        migrations.RunPython(init_problem_repository)
    ]
