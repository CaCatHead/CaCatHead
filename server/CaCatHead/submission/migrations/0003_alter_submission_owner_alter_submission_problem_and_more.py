# Generated by Django 4.1.2 on 2023-01-05 07:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import CaCatHead.core.constants


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0003_problemrepository_is_contest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0006_contestregistration_contest_team_index'),
        ('submission', '0002_alter_submission_options_submission_code_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission_user',
                                    to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='submission_problem',
                                    to='problem.problem', verbose_name='所属题目'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='submission_repository',
                                    to='problem.problemrepository', verbose_name='所属题库'),
        ),
        migrations.CreateModel(
            name='ContestSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(
                    choices=[('contestant', 'Contestant'), ('practice', 'Practice'), ('virtual', 'Virtual'),
                             ('manager', 'Manager'), ('out_of_contest', 'Out Of Contest')], max_length=16,
                    verbose_name='比赛提交类型')),
                ('code', models.TextField(blank=True, verbose_name='代码')),
                ('code_length', models.IntegerField(default=0, verbose_name='代码长度')),
                ('language', models.CharField(max_length=32, verbose_name='程序语言')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('relative_time', models.IntegerField(verbose_name='提交相对时间')),
                ('judged', models.DateTimeField(blank=True, null=True, verbose_name='评测时间')),
                ('verdict', models.CharField(default=CaCatHead.core.constants.Verdict['Waiting'], max_length=32,
                                             verbose_name='提交状态和判题结果')),
                ('score', models.IntegerField(default=0, verbose_name='总分')),
                ('time_used', models.IntegerField(default=0, verbose_name='消耗时间')),
                ('memory_used', models.IntegerField(default=0, verbose_name='消耗内存')),
                ('detail', models.JSONField(blank=True, default=dict, verbose_name='返回详情')),
                ('owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_submission_team',
                                   to='contest.team', verbose_name='创建队伍')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                                              related_name='contest_submission_problem', to='problem.problem',
                                              verbose_name='所属题目')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                                                 related_name='contest_submission_repository',
                                                 to='problem.problemrepository', verbose_name='所属题库')),
            ],
            options={
                'verbose_name': '比赛提交信息',
                'verbose_name_plural': '比赛提交信息列表',
                'db_table': 'contest_submission',
                'ordering': ('-relative_time', '-judged', '-score', '-created', '-id'),
            },
        ),
    ]
