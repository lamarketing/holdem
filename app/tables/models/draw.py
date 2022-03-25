from django.db import models

from common.models import ClassicModelMixin
from tables.models import Player, NameRoundChoices


class Draw(ClassicModelMixin):
    """Одна раздача карт на столе."""
    ended = models.BooleanField(default=False)
    actions = models.ManyToManyField('Action')
    bb = models.PositiveSmallIntegerField()
    round_now = models.CharField(
        max_length=10,
        choices=NameRoundChoices.choices,
        default=NameRoundChoices.preflop
    )
    dealer = models.ForeignKey(
        'Player', on_delete=models.PROTECT
    )
    player_sb = models.ForeignKey(
        'Player', on_delete=models.PROTECT
    )
    player_bb = models.ForeignKey(
        'Player', on_delete=models.PROTECT
    )
    players_fold = models.ManyToManyField(
        'Player'
    )
    pot = models.PositiveSmallIntegerField(default=0)
    to_call = models.PositiveSmallIntegerField(default=0)

    def choose_init_dealer_sb_bb(self, players: models.QuerySet[Player]) -> None:
        """Выбирает дилера, малый и большой блайнды для этой раздачи.
            1. Выбирает dealer, sb, bb
            2. Сохраняет их в поля из self
            3. Меняет дилеру порядок, чтобы в следующую раздачу он не стал дилером
        """
        players = players.filter(stack__gte=0).order_by('order')
        dealer: Player = players[0]
        self.dealer = dealer
        self.player_sb: Player = players[1]
        self.player_bb: Player = players[2]
        self.save()
        dealer.order += 10
        dealer.save()
