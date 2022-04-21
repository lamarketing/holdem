from django.db import models
from abstractuser.models import User
from cards.models import Card, NameCombination

from common.models import ClassicModelMixin


class DrawPlayer(ClassicModelMixin):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT
    )
    draw = models.ForeignKey(
        'Draw', on_delete=models.CASCADE,
        related_name='draw_players'
    )
    hand = models.ManyToManyField(
        Card, blank=True,
        related_name='draw_player_hand'
    )
    high_five = models.ManyToManyField(
        Card, blank=True,
        related_name='draw_player_high'
    )
    high_name = models.CharField(
        max_length=30,
        choices=NameCombination.choices,
        default=NameCombination.high
    )
    high_value = models.BigIntegerField(default=0)

    winner = models.BooleanField(default=False)

    is_fold = models.BooleanField(default=False)

    class Meta:
        abstract = False


class Draw(ClassicModelMixin):
    """Одна раздача карт на столе."""
    table = models.ForeignKey(
        'Table', on_delete=models.CASCADE
    )
    table_row = models.PositiveSmallIntegerField(default=1)
    bb = models.PositiveSmallIntegerField(default=10)
    pot = models.PositiveSmallIntegerField(default=0)

    flop = models.ManyToManyField(Card, blank=True, related_name='draw_flop')
    turn = models.ManyToManyField(Card, blank=True, related_name='draw_turn')
    river = models.ManyToManyField(Card, blank=True, related_name='draw_river')

    players = models.ManyToManyField(
        User, through='DrawPlayer',
        blank=True
    )

    class Meta:
        abstract = False
