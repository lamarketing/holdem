from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from abstractuser.models import User
from tables.models import Player
from tables.serializers import PlayerSerializer, TableSerializer
from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer
from tournaments.utils import is_time_to_registration_tournament


class AsyncTournamentConsumer(AsyncJsonWebsocketConsumer):
    """
    ТУРНИР.
    После старта турнира слой уничтожится,
    но должны создастся слои столов.
    За одним столом должно быть не более 6 игроков.
    ID столов нужно записать куда-то юзерам.
    """
    user: User
    layer_name: str
    table_layer: str | None
    tournament: Tournament | None

    async def connect(self):
        """Соединение."""
        self.user = self.scope['user']
        if self.user == AnonymousUser():
            await self.close()

        # Проверяем есть ли у игрока активная игра
        game: Player = await self._db('active_game')
        if game:
            # ===ИГРА.
            if not game.table.tournament.active_now:
                await self.close()
                return
            await self.accept()
            await self.event_individual({
                'type': 'play',
                'table': TableSerializer(game.table).data
            })
        else:
            # ===ТУРНИР.
            # 1. Получаем первый турнир.
            self.tournament = await self._db('get_tournament')
            self.layer_name = f'tournament_{self.tournament.id}'
            # 2. Добавляем в слой турнира
            await self.channel_layer.group_add(
                self.layer_name, self.channel_name
            )
            # 3. Отправляем всем клиентам новую информацию о турнире
            await self.channel_layer.group_send(
                self.layer_name,
                {
                    'type': 'event_group_tournament',
                    'public_type': 'tournament_info',
                }
            )
            await self.accept()
            await self.event_individual({'type': 'is_registered'})

    async def disconnect(self, code):
        pass

    async def receive_json(self, content: dict, **kwargs):
        print(f'{content=}')
        match content['command']:
            case 'registrate':
                if not is_time_to_registration_tournament(self.tournament.start):
                    return
                await self._db('registrate_user')
                await self.event_individual({'type': 'registrate'})
                await self.channel_layer.group_send(
                    self.layer_name,
                    {
                        'type': 'event_group_tournament',
                        'public_type': 'tournament_info',
                    }
                )
            case 'unregistrate':
                if not is_time_to_registration_tournament(self.tournament.start):
                    return
                await self._db('unregistrate_user')
                await self.event_individual({'type': 'unregistrate'})
                await self.channel_layer.group_send(
                    self.layer_name,
                    {
                        'type': 'event_group_tournament',
                        'public_type': 'tournament_info',
                    }
                )

    async def event_individual(self, event: dict):
        """Отправка события индивидуально клиенту."""
        match event['type']:
            case 'registrate':
                event['is_registered'] = True
            case 'unregistrate':
                event['type'] = 'registrate'
                event['is_registered'] = False
            case 'is_registered':
                tournament = await self._db('get_tournament')
                users = tournament.users.all() if tournament else []
                event['type'] = 'registrate'
                event['is_registered'] = self.user in users
            case 'play':
                # Транзитом game, table.
                ...
        await self.send_json(event)

    async def event_group_tournament(self, event: dict):
        """Отправка события о турнире всем каналам слоя турнира."""
        match event['public_type']:
            case 'tournament_info':
                tournament = await self._db('get_tournament')
                event['type'] = event['public_type']
                # del event['public_type']
                event['tournament'] = TournamentPublicSerializer(tournament).data,
                event['count_players'] = tournament.users.all().count() if tournament else 0
        await self.send_json(event)

    async def event_group_table(self, event: dict):
        """Отправка события всем каналам слоя стола."""
        ...
        await self.send_json(event)

    async def registration_open(self, event: dict):
        """Отправка из Celery события всем каналам слоя турнира."""
        await self.send_json({
            'type': 'registration_open',
            'is_registered': False,
            'tournament': event['tournament']
        })

    async def start_tournament(self, event: dict):
        """Отправка из Celery события всем каналам слоя турнира."""
        game = await self._db('active_game')
        await self.send_json({
            'type': 'start_tournament',
            'table': 1 if game else 0,
        })

    @database_sync_to_async
    def _db(self, todo: str):
        match todo:
            case 'active_game':
                return self.user.games.last()
            case 'get_tournament':
                return Tournament.first_tournament()
            case 'registrate_user':
                self.tournament.users.add(self.user)
            case 'unregistrate_user':
                self.tournament.users.remove(self.user)
