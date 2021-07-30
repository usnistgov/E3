from rest_framework.fields import ListField, DictField
from rest_framework.serializers import Serializer

from API.serializers.CashFlowSerializer import RequiredCashFlowSerializer, OptionalCashFlowSerializer


class OutputSerializer(Serializer):
    reqCashFlowObjects = ListField(child=RequiredCashFlowSerializer(), required=True)
    optCashFlowObjects = ListField(child=OptionalCashFlowSerializer(), required=False)
