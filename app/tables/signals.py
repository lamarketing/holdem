from django.db.models.signals import post_save
from django.dispatch import receiver

from tables.models import Action


@receiver(post_save, sender=Action)
def action_create(sender, instance: Action, created, **kwargs):
    """
    Когда создается действие игрока.
    1. Прибавляем ставку действия к поту стола.
    """
    if created:
        table = instance.created_by.table
        table.pot += instance.bet
        table.save()
