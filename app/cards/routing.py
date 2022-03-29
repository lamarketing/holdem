from django.urls import re_path, path
from cards.consumers import CardsConsumer

websocket_urlpatterns = [
    re_path(r"ws/$", CardsConsumer.as_asgi()),
]