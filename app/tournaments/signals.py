from datetime import timedelta

from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.db.models.signals import post_save
from django.dispatch import receiver

from tournaments.models import Tournament


@receiver(post_save, sender=Tournament)
def task_tournament_register(sender, instance: Tournament, created, **kwargs):
    if created:
        shedule_registration = ClockedSchedule.objects.create(
            clocked_time=instance.start - timedelta(minutes=1)
        )
        shedule_start = ClockedSchedule.objects.create(
            clocked_time=instance.start
        )
        PeriodicTask.objects.create(
            name=str(instance.id) + '_registration',
            task='tournaments.tasks.start_registration',
            one_off=True,
            clocked=shedule_registration
        )
        PeriodicTask.objects.create(
            name=str(instance.id) + '_start',
            task='tournaments.tasks.start_tournament',
            one_off=True,
            clocked=shedule_start
        )
