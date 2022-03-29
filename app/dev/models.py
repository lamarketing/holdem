from django.contrib.auth import get_user_model
from django.db import models

from cards.models import Card


class TableDev(models.Model):
    """Стол для игры.
       Есть 4 разных поля по типу

       Понятно, что если поменять поле message_from_shell,
       то эти изменения должны отобразиться у клиентов.
       А что будет, если
       1. ... изменится какое-то поле у сущности,
       которое состоит в M2M (Users)
       2. ... добавится новая сущность в M2M:
       например, было 2 игрока, стало 3
       3. ... изменится ForeignKey (last_action) - например, была карта Туз, а стала Король
       4. ... изменится сам ForeignKey - был Туз и остался Туз, но изменилось какое-то поле у Туза

       Суть игры:
       Когда игрок отправит карту на сайте, то она запишется в last_action у стола.
       Поэтому у других игроков должна показаться именно эта карта и поле modified


    """
    users = models.ManyToManyField(get_user_model(), null=True)
    last_action = models.ForeignKey(
        Card, on_delete=models.CASCADE
    )
    modified = models.DateTimeField(auto_now_add=True)
    message_from_shell = models.CharField(
        max_length=100, blank=True, null=True
    )

