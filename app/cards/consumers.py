from django.contrib.auth.models import User

from cards.models import Card
from cards.serializers import CardSerializer
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin


class CardsConsumer(
        ObserverModelInstanceMixin,
        GenericAsyncAPIConsumer,
):

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (permissions.AllowAny,)
