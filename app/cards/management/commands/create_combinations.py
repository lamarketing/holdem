from django.core.management import BaseCommand

from cards.models import Combination, NameCombination


class Command(BaseCommand):
    help = 'Создание комбинаций.'

    def handle(self, *args, **options):
        combos: list[Combination] = []
        value: int = 0
        for name in NameCombination:
            combos.append(
                Combination(
                    id=name,
                    value=value
                )
            )
            value += 10000000000000
        Combination.objects.bulk_create(combos)
