# Generated by Django 4.1.2 on 2023-01-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='single_user',
            field=models.BooleanField(default=False, verbose_name='用户自己的队伍'),
        ),
    ]