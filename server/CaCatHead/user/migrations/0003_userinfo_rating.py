# Generated by Django 4.1.2 on 2023-01-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_root'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='rating',
            field=models.IntegerField(default=1500, verbose_name='Rating'),
        ),
    ]
