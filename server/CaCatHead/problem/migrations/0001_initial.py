# Generated by Django 4.1.2 on 2022-10-30 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY
from CaCatHead.problem.models import ProblemRepository


def init_main_problem_repository(_apps, _schema_editor):
    """
    初始化主题库
    """
    main_repo = ProblemRepository(name=MAIN_PROBLEM_REPOSITORY, is_public=False)
    main_repo.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=45, null=True, unique=True, verbose_name='题目编号')),
                ('title', models.CharField(max_length=512, verbose_name='标题')),
                ('time_limit', models.IntegerField(default=1000, verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(default=262144, verbose_name='内存限制')),
                ('is_public', models.BooleanField(default=True,
                                                  help_text='该项被选择后，题目将会被所有人看到，如果不选择则题目只能被超级用户和管理员看到.',
                                                  verbose_name='是否公开')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL,
                                            verbose_name='创建者')),
            ],
            options={
                'verbose_name': '题目信息',
                'verbose_name_plural': '题目列表',
                'db_table': 'problem',
            },
        ),
        migrations.CreateModel(
            name='ProblemContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512, verbose_name='标题')),
                ('description', models.TextField(blank=True, null=True, verbose_name='题目描述')),
                ('input', models.TextField(blank=True, null=True, verbose_name='输入描述')),
                ('output', models.TextField(blank=True, null=True, verbose_name='输出描述')),
                ('sample', models.TextField(blank=True, null=True, verbose_name='样例')),
                ('hint', models.TextField(blank=True, null=True, verbose_name='解答提示')),
                ('source', models.TextField(blank=True, null=True, verbose_name='题目来源')),
                ('extra_content', models.JSONField(blank=True, null=True, verbose_name='其他信息')),
            ],
            options={
                'verbose_name': '题目内容',
                'verbose_name_plural': '题目内容列表',
                'db_table': 'problem_content',
            },
        ),
        migrations.CreateModel(
            name='ProblemJudge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_type',
                 models.CharField(choices=[('classic', 'classic'), ('interactive', 'interactive')], max_length=32,
                                  verbose_name='题目类型')),
                ('time_limit', models.IntegerField(default=1000, verbose_name='时间限制')),
                ('memory_limit', models.IntegerField(default=262144, verbose_name='内存限制')),
                ('score', models.IntegerField(default=0, verbose_name='题目总分')),
                ('testdata_count', models.IntegerField(default=0, verbose_name='用例数目')),
                ('testdata_score', models.JSONField(default=list, verbose_name='用例分数')),
                ('extra_info', models.JSONField(blank=True, null=True, verbose_name='其他信息')),
            ],
            options={
                'verbose_name': '题目评测信息',
                'verbose_name_plural': '题目评测信息列表',
                'db_table': 'problem_judge',
            },
        ),
        migrations.CreateModel(
            name='ProblemRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='题目仓库名称')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否公开')),
                ('problems', models.ManyToManyField(to='problem.problem')),
            ],
            options={
                'verbose_name': '题目仓库',
                'verbose_name_plural': '题目仓库列表',
                'db_table': 'problem_repository',
            },
        ),
        migrations.CreateModel(
            name='ProblemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_content',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problemcontent',
                                   verbose_name='题目描述内容')),
                ('problem_judge',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='problem.problemjudge',
                                   verbose_name='评测信息')),
            ],
            options={
                'verbose_name': '题目信息',
                'verbose_name_plural': '题目信息列表',
                'db_table': 'problem_info',
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='problem_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='problem.probleminfo',
                                    verbose_name='题目信息'),
        ),
        migrations.RunPython(init_main_problem_repository)
    ]
