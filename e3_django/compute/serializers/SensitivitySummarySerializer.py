from rest_framework.fields import ListField
from rest_framework.serializers import Serializer


class SensitivitySummarySerializer(Serializer):
    """
    Object serializer for sensitivity summary.
    """

    # output for sensitivity 
    output = ListField(child=AlternativeSummarySerializer, required=True)