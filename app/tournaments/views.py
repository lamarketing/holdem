from django.db.models import F, Count, Exists

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer


class TournamentMixin:
    queryset = Tournament.objects.all()


class TournamentsPublicView(TournamentMixin, ListAPIView):
    serializer_class = TournamentPublicSerializer
