from django.urls import path

from tournaments.consumers import AsyncTournamentConsumer

websocket_urlpatterns = [
    path("ws/tournament/", AsyncTournamentConsumer.as_asgi()),
]
