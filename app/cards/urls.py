from django.urls import path

from cards.views import CardsAll

urlpatterns = [
    path('cards/', CardsAll.as_view())
]