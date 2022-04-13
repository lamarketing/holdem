from django.urls import path

from tables.consumers import AsyncTableConsumer

websocket_urlpatterns = [
    path("ws/tournament/play", AsyncTableConsumer.as_asgi()),
]
