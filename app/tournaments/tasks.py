from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer

schedule, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS
)

create, _ = PeriodicTask.objects.get_or_create(
    interval=schedule,
    task='tournaments.tasks.start_tournament',
)

channel_layer = get_channel_layer()


@shared_task
def start_tournament():
    """Стартует турнир, который должен стартовать."""
    Tournament.inactivate_all_tournaments()
    tournament: Tournament = Tournament.first_tournament()
    # тут нужна проверка, что start <= now()
    tournament.active_now = True
    tournament.save()

    async_to_sync(channel_layer.group_send)(
        f'tournament_{tournament.id}',
        {
            'type': 'c_send_tournament_info',
            'data': {
                'tournament': TournamentPublicSerializer(tournament).data
            },
        }
    )

def start_registration():
    tournament: Tournament = Tournament.first_tournament()

