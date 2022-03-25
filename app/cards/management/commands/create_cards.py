from itertools import product

from django.core.management import BaseCommand

from cards.models import Card


class Command(BaseCommand):
    help = 'Создание 52 карт.'

    def handle(self, *args, **options):
        cards: list[Card] = []
        value: int = 1
        deck = product(range(2, 15), 'cdrs')
        raw = 0
        for card in deck:
            nominal: int = card[0]
            suit: str = card[1]
            cards.append(
                Card(
                    id=str(nominal) + suit,
                    nominal=nominal,
                    suit=suit,
                    magic=value
                )
            )
            raw += 1
            if raw == 4:
                raw = 0
                value *= 10
        Card.objects.bulk_create(cards)
