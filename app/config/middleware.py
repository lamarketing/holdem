from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user(token):
    try:
        return Token.objects.get(pk=token).user
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class DRFAuthMiddleware:
    """Проверка токена."""

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            scope['user'] = await get_user(scope["query_string"].decode('UTF-8')[6:])
        except:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
