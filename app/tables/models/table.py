from django.contrib.auth import get_user_model
from django.db import models

from cards.models import Card
from common.models import ClassicModelMixin, StartEndMixin
from tables.models import Player
from tournaments.models import Tournament


class Table(ClassicModelMixin, StartEndMixin):
    """Один стол одного турнира."""
    tournament = models.ForeignKey(
        Tournament, on_delete=models.PROTECT, null=True
    )
    tournaments_row = models.PositiveSmallIntegerField(default=1)

    # players = models.ManyToManyField(
    #     get_user_model(), through='Player', blank=True
    # )
    init_bb = models.PositiveSmallIntegerField(default=0)

    how_many_rows = models.PositiveSmallIntegerField(default=0)

    pot = models.PositiveSmallIntegerField(default=0)

    flop = models.ManyToManyField(Card, blank=True, related_name='table_flop')
    turn = models.ManyToManyField(Card, blank=True, related_name='table_turn')
    river = models.ManyToManyField(Card, blank=True, related_name='table_tver')
    all_cards = models.ManyToManyField(Card, blank=True, related_name='table_cards')
    # dealer = models.ForeignKey(Player, on_delete=models.PROTECT)
    # sb = models.ForeignKey(Player, on_delete=models.PROTECT)

    class Meta:
        abstract = False
