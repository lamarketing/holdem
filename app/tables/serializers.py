from rest_framework import serializers

from cards.serializers import GameCardSerializer
from tables.models import Table, Player


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    hand = GameCardSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = (
            'user', 'stack', 'hand'
        )


class PlayerPublicSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = (
            'user', 'stack'
        )


class TableSerializer(serializers.ModelSerializer):
    players = PlayerPublicSerializer(many=True)

    class Meta:
        model = Table
        fields = (
            'id', 'start', 'end',
            'tournaments_row',
            'init_bb',
            'players',
            'pot'
        )
