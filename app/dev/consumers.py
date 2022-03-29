from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

from dev.models import TableDev
from dev.serializers import TableDevSerializer


class TableConsumer(
        ObserverModelInstanceMixin,
        GenericAsyncAPIConsumer,
):

    queryset = TableDev.objects.all()
    serializer_class = TableDevSerializer
