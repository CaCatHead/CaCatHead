from django.db import models
from django.utils.translation import gettext_lazy as _


class JudgeNode(models.Model):
    """判题节点
    """
    name = models.CharField(max_length=256, unique=True, verbose_name=_(u"节点名称"))

    active = models.BooleanField(default=True, verbose_name=_(u"是否活跃"))

    updated = models.DateTimeField(verbose_name=_(u"响应时间"))

    information = models.JSONField(default=dict, verbose_name=_(u"判题节点信息"))

    class Meta:
        db_table = 'judge_node'

        ordering = ('-active',  'name',)

        verbose_name = _("判题节点")

        verbose_name_plural = _("判题节点集群")

    def __str__(self):
        return self.name
