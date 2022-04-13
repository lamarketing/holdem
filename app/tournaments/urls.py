from django.urls import path

from tournaments.views import TournamentsPublicView

urlpatterns = [
    path('tournaments/', TournamentsPublicView.as_view()),
]