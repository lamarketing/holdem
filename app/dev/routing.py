from django.urls import re_path, path

from dev.consumers import TableConsumer

websocket_urlpatterns = [
    path("ws/table/<int:id>/", TableConsumer.as_asgi()),
]
