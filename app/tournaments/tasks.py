from datetime import datetime

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from abstractuser.models import User
from django.db.models import QuerySet

from cards.models import Combination
from tables.models import (
    Table,
    Player, PlayerPosition,
    Action, NameRoundChoices, NameActionChoice
)
from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer
from tournaments.utils import (
    is_time_to_registration_tournament,
    is_time_to_active_tournament
)


channel_layer = get_channel_layer()


@shared_task
def start_registration():
    """Открытие регистрации для первого турнира."""
    tournament: Tournament = Tournament.first_tournament()

    if not is_time_to_registration_tournament(tournament.start):
        return

    tournament.is_registration = True
    tournament.save()

    async_to_sync(channel_layer.group_send)(
        f'tournament_{tournament.id}',
        {
            'type': 'registration_open',
            'tournament': TournamentPublicSerializer(tournament).data,
        }
    )


@shared_task
def start_tournament():
    """
    Старт турнира, который должен стартовать.
    1. Деактивация всех активных турниров
    2. Открытие первого турнира, у которого нет времени конца

    """
    Tournament.inactivate_all_tournaments()
    tournament: Tournament = Tournament.first_tournament()

    if not tournament.is_registration:
        return

    if not is_time_to_active_tournament:
        return

    tournament.active_now = True
    tournament.save()

    # 1. Создание всех необходимых столов для первого круга.
    tables: list = []
    count_players = tournament.users.count()
    int_for_range = (
        count_players // 6 + 1
        if count_players % 6 > 1
        else count_players // 6
    )

    for j in range(int_for_range):
        tables.append(
            Table(
                tournament=tournament,
                init_bb=10,
            )
        )
    tables = Table.objects.bulk_create(tables) if tables else []
    if not tables:
        tables.append(Table.objects.create(tournament=tournament, init_bb=10))

    # 2. Раздача борда: флопа, тёрна, ривера.
    for table in tables:
        deck: list = Combination.deck()
        flop: list = Combination.combination_from_deck(deck, 3)
        turn: list = Combination.combination_from_deck(deck, 1)
        river: list = Combination.combination_from_deck(deck, 1)
        table.flop.add(*Combination.combination_format(flop))
        table.turn.add(*Combination.combination_format(turn))
        table.river.add(*Combination.combination_format(river))
        table.all_cards.add(*Combination.combination_format(deck))

    # 3. Создание из юзеров игроков, назначение им столов, раздача рук.
    i = 1
    table_i = 0
    users: QuerySet[User] = tournament.users.order_by('?')
    for user in users:
        if not (i % 6):
            table_i += 1
        table = tables[table_i]
        player = Player.objects.create(
            table=table,
            user=user,
            stack=tournament.init_stack
        )
        deck = table.all_cards.values_list('id', flat=True)
        hand = Combination.combination_from_deck(list(deck), 2)
        player.hand.add(*hand)
        table.all_cards.remove(*hand)

    # 4. Совершение первых действий(ставок sb, bb).
    for table in tables:
        table_players = table.players.all()
        qty_of_players = len(table_players)
        if qty_of_players == 1:
            table_players.delete()
            table.delete()
            tables.remove(table)
        elif qty_of_players == 2:
            player_1: Player = table_players.first()
            player_1.position = PlayerPosition.dbb
            player_1.save()
            player_2: Player = table_players.last()
            player_2.position = PlayerPosition.sb
            player_2.move = True
            player_2.save()
            Action.objects.create(
                created_by=player_2,
                name=NameActionChoice.sb,
                round=NameRoundChoices.preflop,
                bet=(table.init_bb * table.how_many_rows)/2
            )
            player_1.move = True
            player_1.save()
            Action.objects.create(
                created_by=player_1,
                name=NameActionChoice.bb,
                round=NameRoundChoices.preflop,
                bet=table.init_bb * table.how_many_rows
            )
            player_1.last_move = True
            player_1.bet = table.init_bb * table.how_many_rows
            player_1.save()
            player_2.move = True
            player_2.to_call = (table.init_bb * table.how_many_rows)/2
            player_2.bet = (table.init_bb * table.how_many_rows) / 2
            player_2.save()

            table.bet = table.init_bb * table.how_many_rows
            table.save()

    # 5. Если нет столов - закрыть турнир.
    if not tables:
        tournament.is_registration = False
        tournament.active_now = False
        tournament.end = datetime.now()
        tournament.save()

    async_to_sync(channel_layer.group_send)(
        f'tournament_{tournament.id}',
        {
            'type': 'start_tournament',
        }
    )
