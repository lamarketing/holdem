from rest_framework import serializers

from cards.serializers import GameCardSerializer
from tables.models import (
    Table, Player,
    DrawPlayer, Draw,
    Action,
)


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    hand = GameCardSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = (
            'user', 'stack',
            'hand', 'to_call',
            'position', 'move', 'last_move',
            'is_fold',
        )


class PlayerPublicSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = (
            'user', 'stack',
            'position', 'move', 'last_move',
            'is_fold',
        )


class TableSerializer(serializers.ModelSerializer):
    players = PlayerPublicSerializer(many=True)

    class Meta:
        model = Table
        fields = (
            'players', 'pot', 'bet', 'round',
            'init_bb', 'how_many_rows',
        )


class TableFlopSerializer(serializers.ModelSerializer):
    players = PlayerPublicSerializer(many=True)
    flop = GameCardSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = (
            'players', 'pot', 'bet', 'round',
            'init_bb', 'how_many_rows',
            'flop'
        )


class TableTurnSerializer(serializers.ModelSerializer):
    players = PlayerPublicSerializer(many=True)
    flop = GameCardSerializer(many=True, read_only=True)
    turn = GameCardSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = (
            'players', 'pot', 'bet', 'round',
            'init_bb', 'how_many_rows',
            'flop', 'turn'
        )


class TableRiverSerializer(serializers.ModelSerializer):
    players = PlayerPublicSerializer(many=True)
    flop = GameCardSerializer(many=True, read_only=True)
    turn = GameCardSerializer(many=True, read_only=True)
    river = GameCardSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = (
            'players', 'pot', 'bet', 'round',
            'init_bb', 'how_many_rows',
            'flop', 'turn', 'river'
        )


class PlayerUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = ('user',)


class ActionSerializer(serializers.ModelSerializer):
    created_by = PlayerUserSerializer()

    class Meta:
        model = Action
        fields = (
            'created_by', 'name', 'bet',
        )


class DrawPlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrawPlayer
        fields = (
            'table_row', 'bb', 'pot',
        )


