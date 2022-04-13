from rest_framework import serializers

from tournaments.models import Tournament


class TournamentPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = (
            'id', 'start', 'title', 'active_now', 'is_registration',
            'prize', 'seconds_to_think', 'init_stack'
        )
