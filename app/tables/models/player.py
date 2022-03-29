from django.contrib.auth import get_user_model
from django.db import models

from common.models import ClassicModelMixin


class Player(ClassicModelMixin):
    """Показатели одного игрока в рамках одного стола."""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT
    )
    table = models.ForeignKey(
        'Table', on_delete=models.PROTECT
    )
    stack = models.PositiveSmallIntegerField(default=0)
    is_present = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = False
