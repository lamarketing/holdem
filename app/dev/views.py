from rest_framework import generics

from dev.models import TableDev
from dev.serializers import TableDevSerializer


class TableView(generics.RetrieveAPIView):

    queryset = TableDev.objects.all()
    serializer_class = TableDevSerializer


class TablesViews(generics.ListAPIView):
    queryset = TableDev.objects.all()
    serializer_class = TableDevSerializer
