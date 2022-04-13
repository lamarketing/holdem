from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from abstractuser.models import User
from django.db.models import QuerySet

from cards.models import Combination
from tables.models import Table, Player
from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer
from tournaments.utils import is_time_to_registration_tournament, is_time_to_active_tournament


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
            'type': 'celery_event',
            'public_type': 'registration_open',
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

    # Создание всех необходимых столов для первого круга.
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
    print(f'{tables=}')
    if not tables:
        tables.append(Table.objects.create(tournament=tournament, init_bb=10))

    for table in tables:
        deck: list = Combination.deck()
        flop: list = Combination.combination_from_deck(deck, 3)
        turn: list = Combination.combination_from_deck(deck, 1)
        river: list = Combination.combination_from_deck(deck, 1)
        table.flop.add(*Combination.combination_format(flop))
        table.turn.add(*Combination.combination_format(turn))
        table.river.add(*Combination.combination_format(river))
        table.all_cards.add(*Combination.combination_format(deck))

    # Создание из юзеров игроков и назначение им столов.
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

    # players = Player.objects.bulk_create(games)

    # 1 юзер, которому не достался стол, потому что он был бы там один.
    # last_unlucky_user: str | None = users.last().id if count_players % 6 == 1 else None
    # tournament.users.remove(users.last())
    channel_layer

    async_to_sync(channel_layer.group_send)(
        f'tournament_{tournament.id}',
        {
            'type': 'celery_event',
            'public_type': 'start_tournament',
        }
    )
