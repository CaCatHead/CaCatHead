# Generated by Django 4.1.2 on 2023-01-31 09:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('contest', '0004_alter_ratinglog_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contestregistration',
            unique_together={('contest', 'team'), ('contest', 'name')},
        ),
    ]
