import itertools

from django.core.management import BaseCommand

from cards.models import Card, Combination, Five


class Command(BaseCommand):
    help = 'Создание всех комбинаций из 5 карт'

    @staticmethod
    def _calc_five(five: tuple[Card]) -> tuple[str, int, str]:
        """Предварительный просчет данных для одной пятерки."""
        name: str = ''
        suits: str = ''
        nominals: int = 0
        for card in five:
            name += str(card.nominal) + card.suit
            suits += card.suit
            nominals += card.magic

        return name, nominals, suits

    def handle(self, *args, **options):
        cards = Card.objects.all()
        fives = itertools.combinations(cards, 5)
        combinations = Combination.objects.all()
        fives_to_create: list[Five] = []

        for five in fives:
            name, nominals, suits = self._calc_five(five)
            combination: Combination = combinations.get(
                id=Combination.what(nominals, suits)
            )
            value: int = nominals + combination.value

            fives_to_create.append(
                Five(
                    id=name,
                    sum_of_nom=nominals,
                    combination=combination,
                    value=value
                )
            )
        Five.objects.bulk_create(fives_to_create, batch_size=10000)
