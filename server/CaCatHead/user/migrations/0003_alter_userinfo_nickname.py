# Generated by Django 4.1.2 on 2023-01-31 09:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, default='', max_length=50, unique=True, verbose_name='昵称'),
        ),
    ]