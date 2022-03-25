from django.conf import settings
from django.db import models

from common.models import ClassicModelMixin, StartEndMixin

User = settings.AUTH_USER_MODEL


class Tournament(ClassicModelMixin, StartEndMixin):
    title = models.CharField(max_length=300, default="")
    prize = models.CharField(max_length=300, default="")
    init_stack = models.PositiveSmallIntegerField(default=0)
    seconds_to_think = models.PositiveSmallIntegerField(default=12)

    users = models.ManyToManyField(User)
