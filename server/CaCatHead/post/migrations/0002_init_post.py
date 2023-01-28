from django.core.management import call_command
from django.db import migrations


def load_fixture(_apps, _schema_editor):
    call_command('loaddata', 'post.json', app_label='post')


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0002_root'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
