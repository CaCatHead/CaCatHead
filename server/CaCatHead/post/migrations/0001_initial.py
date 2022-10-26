# Generated by Django 4.1.2 on 2022-10-26 17:40

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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('sortTime', models.DateTimeField(auto_now_add=True, verbose_name='排序时间')),
                ('isPublic', models.BooleanField(default=False, verbose_name='是否公开')),
                ('publisher',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL,
                                   verbose_name='发布者')),
            ],
            options={
                'ordering': ['sortTime'],
            },
        ),
        migrations.CreateModel(
            name='PostContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='公告内容')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='post.post',
                                              verbose_name='公告')),
            ],
        ),
    ]
