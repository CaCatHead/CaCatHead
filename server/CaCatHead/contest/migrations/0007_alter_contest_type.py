# Generated by Django 4.1.2 on 2023-01-05 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contest', '0006_contestregistration_contest_team_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='type',
            field=models.CharField(choices=[('icpc', 'Icpc'), ('ioi', 'Ioi')], default='icpc', max_length=64,
                                   verbose_name='比赛类型'),
        ),
    ]
