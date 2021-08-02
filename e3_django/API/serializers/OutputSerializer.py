from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.serializers import RequiredCashFlowSerializer, OptionalCashFlowSerializer, AlternativeSummarySerializer


class OutputSerializer(Serializer):
    alternativeSummary = ListField(child=AlternativeSummarySerializer(), required=True)
    reqCashFlowObjects = ListField(child=RequiredCashFlowSerializer(), required=True)
    optCashFlowObjects = ListField(child=OptionalCashFlowSerializer(), required=False)
