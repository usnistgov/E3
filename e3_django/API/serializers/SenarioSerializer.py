from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer
from drf_compound_fields.fields import ListOrItemField


class ScenarioSerializer(Serializer):
    objectVariables = ListOrItemField(child=IntegerField(), required=False)
