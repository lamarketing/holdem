from rest_framework.serializers import ModelSerializer

from dev.models import TableDev


class TableDevSerializer(ModelSerializer):

    class Meta:
        model = TableDev
        fields = ('id', 'users', 'last_action', 'modified', 'message_from_shell')
