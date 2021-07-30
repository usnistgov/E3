from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.serializers import RequiredCashFlowSerializer, OptionalCashFlowSerializer


class OutputSerializer(Serializer):
    reqCashFlowObjects = ListField(child=RequiredCashFlowSerializer(), required=True)
    optCashFlowObjects = ListField(child=OptionalCashFlowSerializer(), required=False)
