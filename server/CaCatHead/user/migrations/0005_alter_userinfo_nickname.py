# Generated by Django 4.1.2 on 2023-03-19 07:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0004_usertoken_expiry_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='昵称'),
        ),
    ]
