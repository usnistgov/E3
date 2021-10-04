from rest_framework.fields import Field
from rest_framework.serializers import Serializer


class OutputSerializer(Serializer):
    """
    Object serializer for the main output object.
    """


def register_output_serializer(name: str, field: Field):
    setattr(OutputSerializer, name, field)
