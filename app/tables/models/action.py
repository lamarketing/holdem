from django.contrib.auth import get_user_model
from django.db import models

from common.models import ClassicModelMixin


class NameActionChoice(models.TextChoices):
    fold = 'Fold'
    check = 'Check'
    bet = 'Bet'
    call = 'Call'
    high = 'Raise'
    sm = 'Small Blind'
    bb = 'Big Blind'


class NameRoundChoices(models.TextChoices):
    preflop = 'Preflop'
    flop = 'Flop'
    turn = 'Turn'
    river = 'River'


class Action(ClassicModelMixin):
    """Действие одного игрока."""
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=20,
        choices=NameActionChoice.choices,
        default=NameActionChoice.fold
    )
    bet = models.PositiveSmallIntegerField
    round = models.CharField(
        max_length=10,
        choices=NameRoundChoices.choices,
        default=NameRoundChoices.preflop
    )
