from django.contrib import admin

from cards.models import Five, Card, Combination, Seven


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'nominal', 'suit', 'magic')
    fields = ('nominal', 'suit', 'magic')
    readonly_fields = ('nominal', 'suit', 'magic')


# @admin.register(Combination)
# class CombinationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     readonly_fields = ('id', 'value')
#
#
# @admin.register(Five)
# class FiveAdmin(admin.ModelAdmin):
#     list_display = ('id', 'combination', 'sum_of_nom', 'value')
#     fields = ('combination', 'sum_of_nom', 'value')
#     search_fields = ('id', )
#     list_filter = ('combination',)
#     readonly_fields = ('combination', 'sum_of_nom', 'value')
#
#
# @admin.register(Seven)
# class SevenAdmin(admin.ModelAdmin):
#     list_display = ('id', 'five')
#     list_select_related = ('five',)
#     readonly_fields = ('five', )

