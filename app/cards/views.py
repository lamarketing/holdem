from rest_framework.generics import RetrieveAPIView, ListAPIView

from cards.models import Card
from cards.serializers import CardSerializer


class CardsAll(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
