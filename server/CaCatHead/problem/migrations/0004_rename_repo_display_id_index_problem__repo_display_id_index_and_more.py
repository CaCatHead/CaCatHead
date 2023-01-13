# Generated by Django 4.1.2 on 2023-01-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('problem', '0003_alter_problem_options'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='problem',
            new_name='problem__repo_display_id_index',
            old_name='repo_display_id_index',
        ),
        migrations.AddIndex(
            model_name='problem',
            index=models.Index(fields=['repository'], name='problem__repo_index'),
        ),
    ]
