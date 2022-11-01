from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubmissionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CaCatHead.submission'
    verbose_name = _("提交记录")
