import time

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from abstractuser.models import User
from cards.models import Combination
from tables.models import (
    Player, Action, NameActionChoice,
    Draw, DrawPlayer, NameRoundChoices,
    PlayerPosition, Table
)
from tables.serializers import (
    PlayerSerializer,
    TableSerializer,
    TableFlopSerializer, TableTurnSerializer, TableRiverSerializer,
    ActionSerializer
)
from tournaments.models import Tournament


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
        table: Table = game.table
        self.table_layer = f'table_{table.id}'
        await self.channel_layer.group_add(
            self.table_layer, self.channel_name
        )
        await self.accept()
        await self.event_individual({
            'type': 'game',
            'game': PlayerSerializer(game).data,
        })
        TS = TableSerializer
        if table.round == NameRoundChoices.flop:
            TS = TableFlopSerializer
        elif table.round == NameRoundChoices.turn:
            TS = TableTurnSerializer
        elif table.round == NameRoundChoices.river:
            TS = TableRiverSerializer
        await self.event_individual({
            'type': 'table',
            'table': TS(table).data,
        })
        last_table_action = await self._db(
            'last_table_action', table=table)
        await self.event_individual({
            'type': 'action',
            'action': ActionSerializer(last_table_action).data
        })

    async def disconnect(self, code):
        pass

    async def receive_json(self, content: dict, **kwargs):
        # 1 Получение игры игрока и стола.
        game: Player = await self._db('active_game')
        if not game and not game.to_call:
            return
        table = game.table
        # 2 Присвоение следующему игроку право на ход.
        players = table.players.filter(
            is_fold=False
        ).only(
            'id', 'move', 'is_fold'
        )
        players_len = len(players)
        if not game.last_move:
            is_next_player_move = False
            for index, player in enumerate(players, start=1):
                if is_next_player_move:
                    print('Next Move', player.user)
                    player.move = True
                    player.save()
                    break
                if index == players_len:
                    print('First Move', player.user)
                    player = players.first()
                    player.move = True
                    player.save()
                    break
                if player.move:
                    print('Move', player.user)
                    is_next_player_move = True
                    continue

        match content['command']:
            case 'call':
                action = Action.objects.create(
                    created_by=game,
                    name=NameActionChoice.call,
                    round=game.table.round,
                    bet=game.to_call,
                    table_row=table.how_many_rows
                )

                await self._game_table_action_(
                    TableSerializer(table).data,
                    ActionSerializer(action).data
                )

                if game.last_move:
                    if table.round == NameRoundChoices.river:
                        time.sleep(3)
                        # 1. Создание раздачи.
                        draw = Draw.objects.create(
                            table=table,
                            table_row=table.how_many_rows,
                            bb=table.how_many_rows*table.init_bb,
                            pot=table.pot
                        )
                        draw.flop.add(*table.flop.all())
                        draw.turn.add(*table.turn.all())
                        draw.river.add(*table.river.all())
                        # 2. Получение всех играющих игроков.
                        players = table.players.filter(
                            is_fold=False
                        ).select_related(
                            'hand'
                        ).only(
                            'id',
                            'hand__id', 'hand__magic', 'hand__suit'
                        )
                        board = [
                            *table.flop.all(),
                            *table.turn.all(),
                            *table.river.all()
                        ]
                        highest: tuple[DrawPlayer, Player] | None = None
                        highests: list[tuple[DrawPlayer, Player]] = []
                        # 3. Определение победителя
                        for player in players:
                            # 3.1 Поиск старшей комбинации.
                            high_five, high_name, high_value = Combination.highest_combo_from_seven(
                                [
                                    *player.hand.all(),
                                    *board
                                ]
                            )
                            # 3.2 Создание итога игры игрока.
                            draw_player = DrawPlayer.objects.create(
                                user=player.user,
                                draw=draw,
                                high_name=high_name,
                                high_value=high_value,
                            )
                            draw_player.hand.add(*player.hand.all())
                            draw_player.high_five.add(*high_five)
                            # 3.3 Сравнение старшей комбинации с другими.
                            if highest is None:
                                highest = (draw_player, player)
                            elif highest[0].high_value < high_value:
                                highest = (draw_player, player)
                                highests = []
                            elif highest[0].high_value == high_value:
                                highests.append(highest)
                                highests.append((draw_player, player))

                        # 4. Сохранение записи победителю.
                        if not highests:
                            # 4.1 Когда один победитель.
                            winner_1: DrawPlayer = highest[0]
                            winner_1.winner = True
                            winner_1.save()
                        else:
                            # 4.2 Когда несколько победителей.
                            for winner in highests:
                                winner[0].winner = True
                                winner[0].save()

            case 'check':
                action = Action.objects.create(
                    created_by=game,
                    name=NameActionChoice.check,
                    round=game.table.round,
                    table_row=table.how_many_rows
                )
                await self._game_table_action_(
                    TableSerializer(table).data,
                    ActionSerializer(action).data
                )

                if game.last_move:
                    if table.round in [
                        NameRoundChoices.preflop,
                        NameRoundChoices.flop,
                        NameRoundChoices.turn
                    ]:
                        time.sleep(1)
                        TS = TableSerializer
                        RN = NameRoundChoices.preflop
                        if table.round == NameRoundChoices.preflop:
                            TS = TableFlopSerializer
                            RN = NameRoundChoices.flop
                        elif table.round == NameRoundChoices.flop:
                            TS = TableTurnSerializer
                            RN = NameRoundChoices.turn
                        elif table.round == NameRoundChoices.turn:
                            TS = TableRiverSerializer
                            RN = NameRoundChoices.river
                        # Назначение ходов игрокам.
                        table.round = RN
                        table.save()
                        if players_len == 2:
                            for player in players:
                                if player.position == PlayerPosition.dbb:
                                    player.last_move = True
                                    player.move = False
                                    player.to_call = 0
                                    player.save()
                                elif player.position == PlayerPosition.sb:
                                    player.last_move = False
                                    player.move = True
                                    player.to_call = 0
                                    player.save()
                        # Отправка флопа.
                        await self.channel_layer.group_send(
                            self.table_layer,
                            {
                                'type': 'game',
                            }
                        )
                        await self.channel_layer.group_send(
                            self.table_layer,
                            {
                                'type': 'table',
                                'table': TS(table).data
                            }
                        )

    async def event_individual(self, event: dict):
        """Отправка события индивидуально клиенту."""
        match event['type']:
            case 'table':
                # Транзитом table.
                ...
            case 'game':
                # Транзитом game.
                ...
            case 'action':
                ...

        await self.send_json(event)

    async def table(self, event: dict):
        await self.send_json(
            {
                'type': 'table',
                'table': event['table'],
            }
        )

    async def game(self, event: dict):
        game = await self._db('active_game')
        await self.send_json(
            {
                'type': event['type'],
                'game': PlayerSerializer(game).data,
            }
        )

    async def end(self, event: dict):
        await self.send_json(
            {
                'type': event['type']
            }
        )

    async def action(self, event: dict):
        await self.send_json(
            {
                'type': event['type'],
                'action': event['action']

            }
        )

    async def _game_table_action_(
            self, table_s, action_s
    ):
        await self.channel_layer.group_send(
            self.table_layer,
            {
                'type': 'game',
            }
        )
        await self.channel_layer.group_send(
            self.table_layer,
            {
                'type': 'table',
                'table': table_s
            }
        )
        await self.channel_layer.group_send(
            self.table_layer,
            {
                'type': 'action',
                'action': action_s
            }
        )

    @database_sync_to_async
    def _db(self, todo: str, **kwargs):
        match todo:
            case 'active_game':
                return self.user.games.select_related(
                    'table'
                ).last()
            case 'last_table_action':
                return Action.objects.filter(
                    created_by__table=kwargs['table']
                ).only(
                    'created_by__user__first_name',
                    'created_by__user__last_name',
                    'name', 'bet'
                ).last()
