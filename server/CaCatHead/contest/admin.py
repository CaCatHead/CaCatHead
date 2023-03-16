from django.contrib import admin

from CaCatHead.contest.models import Contest, ContestRegistration, Team


class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'owner', 'is_public',)

    list_display_links = ('id', 'title',)

    search_fields = ('id', 'title',)


class ContestRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'contest', 'score', 'dirty',)

    list_display_links = ('id', 'name',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'rating',)

    list_display_links = ('id', 'name',)


admin.site.register(Contest, ContestAdmin)
admin.site.register(ContestRegistration, ContestRegistrationAdmin)
admin.site.register(Team, TeamAdmin)
