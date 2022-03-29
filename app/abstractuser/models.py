import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class RankChoices(models.TextChoices):
    fish = 'Fish'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    rank = models.CharField(
        max_length=30,
        choices=RankChoices.choices,
        default=RankChoices.fish
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
