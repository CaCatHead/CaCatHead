import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CaCatHead.settings')

app = Celery('CaCatHead')

app.config_from_object('CaCatHead.core.celery.config')
