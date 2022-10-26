from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from CaCatHead.core.models import BaseModel


class Post(BaseModel):
    """公告
    title: 标题
    publisher: 创建者
    sortTime: 用于排序的时间
    isPublic: 是否公开
    """
    title = models.CharField(max_length=256, verbose_name=_(u"标题"))

    publisher = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name=_(u"发布者"))

    sortTime = models.DateTimeField(auto_now_add=True, verbose_name=_(u"排序时间"))

    isPublic = models.BooleanField(default=False, verbose_name=_(u"是否公开"))

    class Meta:
        ordering = ['sortTime']


class PostContent(models.Model):
    post = models.OneToOneField(Post, related_name='content', null=False, on_delete=models.CASCADE,
                                verbose_name=_(u"公告"))

    content = models.TextField(blank=True, null=True, verbose_name=_(u"公告内容"))
