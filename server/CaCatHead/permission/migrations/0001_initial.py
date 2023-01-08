# Generated by Django 4.1.2 on 2023-01-08 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=32, verbose_name='资源类型')),
                ('content_id', models.BigIntegerField(verbose_name='资源 id')),
                ('codename', models.CharField(max_length=32, verbose_name='权限内容')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='用户')),
            ],
            options={
                'db_table': 'user_permission',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=32, verbose_name='资源类型')),
                ('content_id', models.BigIntegerField(verbose_name='资源 id')),
                ('codename', models.CharField(max_length=32, verbose_name='权限内容')),
                ('group',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='组')),
            ],
            options={
                'db_table': 'group_permission',
                'default_permissions': (),
            },
        ),
        migrations.AddIndex(
            model_name='userpermission',
            index=models.Index(fields=['user', 'content_type', 'content_id', 'codename'], name='user_permission_index'),
        ),
        migrations.AddIndex(
            model_name='grouppermission',
            index=models.Index(fields=['group', 'content_type', 'content_id', 'codename'],
                               name='group_permission_index'),
        ),
    ]
