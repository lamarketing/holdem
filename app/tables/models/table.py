from django.contrib.auth import get_user_model
from django.db import models

from common.models import ClassicModelMixin, StartEndMixin
from tournaments.models import Tournament


class Table(ClassicModelMixin, StartEndMixin):
    """Один стол одного турнира."""
    tournament = models.ForeignKey(
        Tournament, on_delete=models.PROTECT, null=True
    )
    tournaments_row = models.PositiveSmallIntegerField(default=1)

    players = models.ManyToManyField(
        get_user_model(), through='Player'
    )
    init_bb = models.PositiveSmallIntegerField(default=0)

    how_many_rows = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = False
