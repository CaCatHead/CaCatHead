from django.contrib import admin

from CaCatHead.judge.models import JudgeNode


class JudgeNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'updated')

    list_display_links = ('id', 'name',)

    search_fields = ('id', 'name')


admin.site.register(JudgeNode, JudgeNodeAdmin)
