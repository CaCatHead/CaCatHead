from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProblemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CaCatHead.problem'
    verbose_name = _("题目")
