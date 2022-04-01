from django.urls import path

from tournaments.views import TournamentsPublicView, TournamentView

urlpatterns = [
    path('tournaments/', TournamentsPublicView.as_view()),
    path('tournaments/play', TournamentView.as_view())
]