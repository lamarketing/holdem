from django.db import models


class Five(models.Model):
    """Любые пять карт из колоды."""
    id = models.CharField(primary_key=True, max_length=14)
    sum_of_nom = models.BigIntegerField(default=0)
    combination = models.ForeignKey(
        'Combination',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    value = models.BigIntegerField(default=0)

    def __str__(self):
        return self.id

