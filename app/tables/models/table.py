from django.db import models

from cards.models import Card
from common.models import ClassicModelMixin, StartEndMixin
from tables.models import NameRoundChoices
from tournaments.models import Tournament


class Table(ClassicModelMixin, StartEndMixin):
    """Один стол одного турнира."""
    tournament = models.ForeignKey(
        Tournament, on_delete=models.PROTECT, null=True
    )
    tournaments_row = models.PositiveSmallIntegerField(default=1)

    init_bb = models.PositiveSmallIntegerField(default=0)

    how_many_rows = models.PositiveSmallIntegerField(default=1)

    pot = models.PositiveSmallIntegerField(default=0)
    bet = models.PositiveSmallIntegerField(default=0)

    flop = models.ManyToManyField(Card, blank=True, related_name='table_flop')
    turn = models.ManyToManyField(Card, blank=True, related_name='table_turn')
    river = models.ManyToManyField(Card, blank=True, related_name='table_river')
    all_cards = models.ManyToManyField(Card, blank=True, related_name='table_cards')

    round = models.CharField(
        max_length=20,
        choices=NameRoundChoices.choices,
        default=NameRoundChoices.preflop
    )

    class Meta:
        abstract = False
