import copy
import logging

from rest_framework.fields import Field
from rest_framework.serializers import Serializer


output_fields = {}


def register_output_serializer(name: str, field: Field):
    output_fields[name] = field


class OutputSerializer(Serializer):
    """
    Object serializer for the main output object.
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop("fields", None)

        super(OutputSerializer, self).__init__(*args, **kwargs)

        for name, value in output_fields.items():
            self.fields[name] = copy.deepcopy(value)
