# Generated by Django 4.1.2 on 2023-01-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JudgeNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='节点名称')),
                ('active', models.BooleanField(default=True, verbose_name='是否活跃')),
                ('updated', models.DateTimeField(verbose_name='响应时间')),
                ('information', models.JSONField(default=dict, verbose_name='判题节点信息')),
            ],
            options={
                'verbose_name': '判题节点',
                'verbose_name_plural': '判题节点集群',
                'db_table': 'judge_node',
                'ordering': ('-active', 'name'),
            },
        ),
    ]
