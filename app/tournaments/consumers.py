from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer


class AsyncTournamentConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """Соединение."""
        self.user = self.scope['user']
        await self._init_room_conn()
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive_json(self, content: dict, **kwargs):
        print(f'{content=}')
        match content['command']:
            case 'registrate':
                await self.registrateUser()
                await self.channel_layer.group_send(
                    self.layer_name, {'type': 'sendTournamentInfo'}
                )
            case 'unregistrate':
                await self.unregistrateUser()
                await self.channel_layer.group_send(
                    self.layer_name, {'type': 'sendTournamentInfo'}
                )

    async def _init_room_conn(self):
        if self.user == AnonymousUser():
            await self.close()

        # Получаем турнир
        self.tournament = await self.getTournament()

        self.layer_name = f'tournament_{self.tournament.id}'
        await self.channel_layer.group_add(
            self.layer_name, self.channel_name
        )

        await self.channel_layer.group_send(
            self.layer_name, {'type': 'sendTournamentInfo'}
        )

    async def sendTournamentInfo(self, event: dict):
        event['data'] = {
            'tournament': TournamentPublicSerializer(self.tournament).data,
            'is_registered': self.user in self.tournament.users.all()
        }
        await self.send_json(event)

    @database_sync_to_async
    def getTournament(self) -> Tournament:
        return Tournament.objects.filter(
            end__isnull=True
        ).first()

    @database_sync_to_async
    def registrateUser(self):
        self.tournament.users.add(self.user)

    @database_sync_to_async
    def unregistrateUser(self):
        self.tournament.users.remove(self.user)

    async def c_send_tournament_info(self, event):
        await self.send_json(event)

    async def message(self, event):
        await self.send_json(event)
