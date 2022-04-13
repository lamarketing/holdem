from datetime import datetime, timedelta, timezone

from django_celery_beat.models import ClockedSchedule
from django.core.management import BaseCommand

from tables.models import Player, Table
from tournaments.models import Tournament


class Command(BaseCommand):
    help = 'Удаление игр, столов и активного турнира.'

    def handle(self, *args, **options):
        Player.objects.all().delete()
        Table.objects.all().delete()
        Tournament.objects.filter(active_now=True).delete()
        ClockedSchedule.objects.all().delete()
        now = datetime.now(timezone.utc) + timedelta(seconds=90)
        Tournament.objects.create(
            start=now
        )

