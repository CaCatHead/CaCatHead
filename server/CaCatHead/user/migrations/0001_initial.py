# Generated by Django 4.1.2 on 2022-10-28 14:18

import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(blank=True, default='', max_length=50, verbose_name='昵称')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='是否教师')),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户组',
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student_id', models.CharField(blank=True, default=None, max_length=32, null=True, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\d+$'), 'Enter a valid student id')],
                                                verbose_name='学号')),
                ('student_name', models.CharField(blank=True, max_length=32, verbose_name='学生姓名')),
                ('class_id', models.CharField(blank=True, max_length=32, validators=[
                    django.core.validators.RegexValidator(re.compile('^\\d+$'), 'Enter a valid class id')],
                                              verbose_name='班级编号')),
                ('student_college', models.CharField(blank=True, max_length=64, verbose_name='所在学院')),
                ('student_major', models.CharField(blank=True, max_length=32, verbose_name='主修专业')),
                ('student_major_field', models.CharField(blank=True, max_length=32, verbose_name='专业方向')),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '学生信息',
                'verbose_name_plural': '学生组',
                'db_table': 'student_info',
            },
        ),
    ]
