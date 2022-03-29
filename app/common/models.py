import uuid

from django.db import models


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ClassicModelMixin(UUIDMixin, CreatedUpdatedMixin):

    class Meta:
        abstract = True


class StartEndMixin(models.Model):
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
