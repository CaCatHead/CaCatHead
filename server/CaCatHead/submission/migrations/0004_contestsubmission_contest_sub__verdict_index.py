# Generated by Django 4.1.2 on 2023-01-31 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('submission', '0003_alter_contestsubmission_code_alter_submission_code'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='contestsubmission',
            index=models.Index(fields=['verdict'], name='contest_sub__verdict_index'),
        ),
    ]
