# Generated by Django 4.1.2 on 2023-01-28 11:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contest', '0003_team_rating_ratinglog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratinglog',
            options={'ordering': ('-created', 'contest', '-rating'), 'verbose_name': 'Rating 日志',
                     'verbose_name_plural': 'Rating 日志列表'},
        ),
        migrations.AddIndex(
            model_name='ratinglog',
            index=models.Index(fields=['contest'], name='rating_log_contest_index'),
        ),
    ]
