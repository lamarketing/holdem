from django.contrib import admin

from tables.models import Table, Player


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'end')
    # list_display_links = ('title',)
    autocomplete_fields = ('flop', 'turn', 'river')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stack')
    autocomplete_fields = ('hand',)
    readonly_fields = ('created', 'modified')

