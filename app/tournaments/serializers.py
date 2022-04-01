from rest_framework import serializers

from tournaments.models import Tournament


class TournamentPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = (
            'id', 'start', 'title', 'active_now',
            'prize', 'seconds_to_think', 'init_stack'
        )


class TournamentUserSerializer(serializers.ModelSerializer):
    user_register = serializers.ListField()

    class Meta:
        model = Tournament
        fields = ('id', 'title', 'prize', 'start', 'user_register')
