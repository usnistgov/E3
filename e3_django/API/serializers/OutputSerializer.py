from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.serializers.CashFlowSerializer import CashFlowSerializer


class OutputSerializer(Serializer):
    reqCashFlowObjects = ListField(child=CashFlowSerializer(), required=True)
