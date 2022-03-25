from django.db import models


class Seven(models.Model):
    """Любые пять карт из колоды."""
    id = models.CharField(primary_key=True, max_length=14)
    five = models.ForeignKey(
        'Five', on_delete=models.CASCADE
    )

