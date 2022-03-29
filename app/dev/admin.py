from django.contrib import admin

from dev.models import TableDev


@admin.register(TableDev)
class TableDevAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_action', 'modified', 'message_from_shell')
    readonly_fields = ('modified',)
    filter_horizontal = ('users', )
