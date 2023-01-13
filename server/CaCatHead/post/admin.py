from django.contrib import admin

from CaCatHead.post.models import Post, PostContent


class PostContentInline(admin.StackedInline):
    model = PostContent
    verbose_name_plural = '公告内容'
    can_delete = False


class PostAdmin(admin.ModelAdmin):
    """
    TODO:
    + https://docs.djangoproject.com/zh-hans/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.view_on_site
    """
    list_display = ('id', 'title', 'owner', 'is_public', 'is_home', 'sort_time', 'created', 'updated')

    # 控制 list_display 中的字段是否以及哪些字段应该被链接到对象的 “更改” 页面
    # https://docs.djangoproject.com/zh-hans/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display_links
    list_display_links = ('id', 'title')

    search_fields = ('id', 'title')

    list_filter = ('owner', 'is_public')

    inlines = [PostContentInline]


admin.site.register(Post, PostAdmin)
