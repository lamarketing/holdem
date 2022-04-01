import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django_app = get_asgi_application()

from .middleware import DRFAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter

import tournaments.routing

application = ProtocolTypeRouter({
    "http": django_app,
    "websocket": DRFAuthMiddleware(
        URLRouter(
            tournaments.routing.websocket_urlpatterns
        )
    ),
})
