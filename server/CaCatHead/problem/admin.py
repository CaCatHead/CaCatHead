from django.contrib import admin

from CaCatHead.problem.models import Problem, ProblemRepository


class ProblemRepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    list_display_links = ('id', 'name')

    search_fields = ('id', 'name')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_public')

    list_display_links = ('id', 'title',)

    search_fields = ('id', 'title')



admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemRepository, ProblemRepositoryAdmin)
