from rest_framework.serializers import Serializer

from API.serializers.CashFlowSerializer import CashFlowSerializer


class OutputSerializer(Serializer):
    reqCashFlowObjects = CashFlowSerializer()
