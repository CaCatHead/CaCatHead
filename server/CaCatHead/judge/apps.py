from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JudgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CaCatHead.judge'
    verbose_name = _("判题节点")
