from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from abstractuser.models import User
from cards.models import Card
from common.models import ClassicModelMixin


class PlayerPosition(models.TextChoices):
    dealer = 'D', _('Dealer')
    sb = 'SB', _('SmallBlind')
    bb = 'BB', _('BigBlind')
    dsb = 'D SB', _('Dealer&SB')
    dbb = 'D BB', _('Dealer&BB')
    position = 'P', _('Position')


class Player(ClassicModelMixin):
    """Показатели одного игрока в рамках одного стола."""
    user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='games',
        related_query_name='game'
    )
    table = models.ForeignKey(
        'Table', on_delete=models.PROTECT,
        related_name='players',
    )
    stack = models.PositiveSmallIntegerField(default=0)
    is_present = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=1)

    hand = models.ManyToManyField(Card, blank=True)
    hand_value = models.PositiveSmallIntegerField(default=0)

    # position = models.CharField(
    #     max_length=20,
    #     choices=PlayerPosition.choices,
    #     default=PlayerPosition.position
    # )

    class Meta:
        abstract = False
