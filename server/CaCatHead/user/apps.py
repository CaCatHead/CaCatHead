from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CaCatHead.user'
    verbose_name = _('用户')
