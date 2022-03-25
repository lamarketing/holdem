from django.db import models
from django.utils.translation import gettext_lazy as _


class NameCombination(models.TextChoices):
    high = 'High', _('High Card')
    pair = 'Pair', _('Pair')
    pairs = 'Pairs', _('Two Pair')
    set = 'Set', _('Three of a Kind')
    straight = 'Straight', _('Straight')
    flush = 'Flush', _('Flush')
    fullhouse = 'Full House', _('Full House')
    kare = 'Kare', _('Four of a Kind')
    straight_flush = 'Straight Flush', _('Straight Flush')
    royal_straight_flush = 'Royal Straight Flush', _('Royal Straight Flush')


class Combination(models.Model):
    """Конкретная комбинация, где id это имя, а value - значимость."""
    id = models.CharField(
        primary_key=True,
        choices=NameCombination.choices,
        max_length=30
    )
    value = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'combination'
        ordering = ('value',)

    def __str__(self):
        return self.pk

    @staticmethod
    def what(nominals: int, suits: str) -> NameCombination:
        """Определение конкретной комбинации."""
        is_flush: bool = True if suits in ('ccccc', 'ddddd', 'rrrrr', 'sssss') else False

        if nominals == 1111100000000 and is_flush:
            return NameCombination.royal_straight_flush

        nominals_str: str = str(nominals).zfill(13)
        is_straight: bool = '11111' in nominals_str or nominals == 1000000001111

        if is_flush and is_straight:
            return NameCombination.straight_flush

        def search(string: str, number: str):
            return number in string

        if search(nominals_str, '4'):
            return NameCombination.kare

        is_set = search(nominals_str, '3')
        is_pair = search(nominals_str, '2')

        if is_set and is_pair:
            return NameCombination.fullhouse

        if is_flush:
            return NameCombination.flush

        if is_straight:
            return NameCombination.straight

        if is_set:
            return NameCombination.set

        if is_pair:
            if nominals_str.count('2') == 2:
                return NameCombination.pairs
            return NameCombination.pair

        return NameCombination.high
