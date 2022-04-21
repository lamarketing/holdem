from django.db import models

from common.models import ClassicModelMixin


class NameActionChoice(models.TextChoices):
    fold = 'Fold'
    check = 'Check'
    bet = 'Bet'
    call = 'Call'
    high = 'Raise'
    all_in = "All In"
    sb = 'Small Blind'
    bb = 'Big Blind'


class NameRoundChoices(models.TextChoices):
    preflop = 'Preflop'
    flop = 'Flop'
    turn = 'Turn'
    river = 'River'


class Action(ClassicModelMixin):
    """Действие одного игрока."""
    created_by = models.ForeignKey(
        'Player', on_delete=models.PROTECT,
        related_name='actions'
    )
    name = models.CharField(
        max_length=20,
        choices=NameActionChoice.choices,
        default=NameActionChoice.fold
    )
    bet = models.PositiveSmallIntegerField(default=0)
    round = models.CharField(
        max_length=10,
        choices=NameRoundChoices.choices,
        default=NameRoundChoices.preflop
    )
    table_row = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = False
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Не сохранять действие, когда не ход игрока.
        Если сохранение, то у игрока удалять ход.
        """
        player = self.created_by
        if not player.move:
            return
        else:
            player.move = False
            player.stack = player.stack - self.bet
            player.bet = player.bet + self.bet
            player.to_call = 0
            player.save()
            super().save(*args, **kwargs)
