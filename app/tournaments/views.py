from django.db.models import F, Count, Exists

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from tournaments.models import Tournament
from tournaments.serializers import TournamentPublicSerializer, TournamentUserSerializer


class TournamentMixin:
    queryset = Tournament.objects.all()


class TournamentsPublicView(TournamentMixin, ListAPIView):
    serializer_class = TournamentPublicSerializer


class TournamentView(TournamentMixin, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TournamentUserSerializer

    def get_object(self):
        user = self.request.user
        return self.queryset.filter(
            end__isnull=True
        ).annotate(user_register=F('users')).first()
