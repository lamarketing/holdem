from itertools import product, combinations
import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from cards.models import Card


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

    @staticmethod
    def deck() -> list:
        return list(product(range(2, 15), 'cdrs'))

    @staticmethod
    def combination_from_deck(deck: list, qry_of_cards: int = 2) -> list:
        cards = random.sample(deck, qry_of_cards)
        for card in cards:
            deck.remove(card)
        return cards

    @staticmethod
    def combination_format(combo: list):
        return [str(card[0]) + card[1] for card in combo]

    @staticmethod
    def _calc_five(five: tuple[Card]) -> tuple[int, str]:
        """Предварительный просчет данных для одной пятерки."""
        suits: str = ''
        nominals: int = 0
        for card in five:
            suits += card.suit
            nominals += card.magic

        return nominals, suits

    @staticmethod
    def _value_of_combo(name: str) -> int:
        match name:
            case NameCombination.high:
                return 0
            case NameCombination.pair:
                return 10000000000000
            case NameCombination.pairs:
                return 100000000000000
            case NameCombination.set:
                return 1000000000000000
            case NameCombination.straight:
                return 10000000000000000
            case NameCombination.flush:
                return 100000000000000000
            case NameCombination.fullhouse:
                return 1000000000000000000
            case NameCombination.kare:
                return 10000000000000000000
            case NameCombination.straight_flush:
                return 100000000000000000000
            case NameCombination.royal_straight_flush:
                return 1000000000000000000000

    @classmethod
    def highest_combo_from_seven(cls, seven: list[Card]):
        """
        Ищет самую сильную комбинации из суммы руки и борда.
        """
        combos: list[tuple] = list(combinations(seven, 5))
        highest: tuple[Card] | None = None
        highest_name: str = ""
        highest_value: int = 0
        for combo in combos:
            nominals, suits = cls._calc_five(combo)
            name = cls.what(nominals, suits)
            value_combo = cls._value_of_combo(name)
            value = nominals + value_combo
            if highest is None:
                highest = combo
                highest_name = name
                highest_value = value
                continue
            if highest_value < value:
                highest = combo
                highest_name = name
                highest_value = value
            return highest, highest_name, highest_value
