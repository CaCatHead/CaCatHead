# Generated by Django 4.1.2 on 2023-03-19 07:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('contest', '0005_alter_contestregistration_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestregistration',
            options={'ordering': ('-is_participate', '-score', 'dirty'), 'verbose_name': '比赛注册信息',
                     'verbose_name_plural': '比赛注册信息列表'},
        ),
    ]