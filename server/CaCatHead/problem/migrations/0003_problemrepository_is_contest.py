# Generated by Django 4.1.2 on 2023-01-03 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0002_init_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemrepository',
            name='is_contest',
            field=models.BooleanField(default=False, verbose_name='是否为比赛'),
        ),
    ]
