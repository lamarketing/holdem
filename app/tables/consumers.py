from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from abstractuser.models import User
from tables.models import Player
from tables.serializers import PlayerSerializer, TableSerializer
from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer
from tournaments.utils import is_time_to_registration_tournament


class AsyncTableConsumer(AsyncJsonWebsocketConsumer):
    """
    Стол.
    """
    user: User
    table_layer: str | None
    tournament: Tournament | None

    async def connect(self):
        """Соединение."""
        self.user = self.scope['user']
        if self.user == AnonymousUser():
            await self.close()

        # Проверяем есть ли у игрока активная игра
        game: Player = await self._db('active_game')
        if not game:
            await self.close()
            return
        if not game.table.tournament.active_now:
            await self.close()
            return

        self.table_layer = f'table_{game.table.id}'
        await self.channel_layer.group_add(
            self.table_layer, self.channel_name
        )
        await self.accept()
        await self.event_individual({
            'type': 'game_table',
            'game': PlayerSerializer(game).data,
            'table': TableSerializer(game.table).data
        })

    async def disconnect(self, code):
        pass

    async def receive_json(self, content: dict, **kwargs):
        print(f'{content=}')
        # match content['command']:
        #     ...

    async def event_individual(self, event: dict):
        """Отправка события индивидуально клиенту."""
        match event['type']:
            case 'game_table':
                # Транзитом game, table.
                ...
        await self.send_json(event)

    async def event_group_table(self, event: dict):
        """Отправка события всем каналам слоя стола."""
        ...
        await self.send_json(event)

    async def celery_event(self, event: dict):
        """Отправка из Celery события всем каналам слоя турнира."""
        match event['public_type']:
            case 'start_tournament':
                event['type'] = event['public_type']
                game = await self._db('active_game')
                event['game'] = PlayerSerializer(game).data
        await self.send_json(event)

    @database_sync_to_async
    def _db(self, todo: str):
        match todo:
            case 'active_game':
                return self.user.games.last()
            case 'get_tournament':
                return Tournament.first_tournament()
