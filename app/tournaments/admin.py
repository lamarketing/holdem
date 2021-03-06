from django.contrib import admin

from tournaments.models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'prize', 'start')
    list_display_links = ('title',)
