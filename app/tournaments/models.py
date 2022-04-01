from django.conf import settings
from django.db import models

from common.models import ClassicModelMixin, StartEndMixin

User = settings.AUTH_USER_MODEL


class Tournament(ClassicModelMixin, StartEndMixin):
    is_registration = models.BooleanField(default=False)
    active_now = models.BooleanField(default=False)
    title = models.CharField(max_length=300, default="")
    prize = models.CharField(max_length=300, default="")
    init_stack = models.PositiveSmallIntegerField(default=0)
    seconds_to_think = models.PositiveSmallIntegerField(default=12)

    users = models.ManyToManyField(User, blank=True, related_name='tournaments')

    class Meta:
        abstract = False

    @classmethod
    def first_tournament(cls):
        """Ближайший турнир"""
        return cls.objects.filter(
            end__isnull=True,
        ).first()

    @classmethod
    def inactivate_all_tournaments(cls):
        """Все активные турниры сделать неактивными."""
        cls.objects.filter(active_now=True).update(active_now=False)

    @classmethod
    def active_tournament(cls):
        """Активные турнир"""
        return cls.objects.filter(
            active_now=True,
        ).first()
