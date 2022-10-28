from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CaCatHead.post'
    verbose_name = _("公告")
