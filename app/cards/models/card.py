from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Card(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    nominal = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(14)]
    )
    suit = models.CharField(
        max_length=1, validators=[RegexValidator(regex="cdrs")]
    )
    magic = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'card'
        ordering = ('magic', 'id')

    def __str__(self):
        return self.pk
