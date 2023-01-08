from django.contrib import admin

from CaCatHead.contest.models import Contest


class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'owner', 'is_public')

    list_display_links = ('id', 'title',)

    search_fields = ('id', 'title')


admin.site.register(Contest, ContestAdmin)
