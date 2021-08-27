from rest_framework.fields import IntegerField, CharField, ListField, BooleanField
from rest_framework.serializers import Serializer


class AlternativeSerializer(Serializer):
    altID = IntegerField(min_value=0, required=True)
    altName = CharField(required=False)
    altBCNList = ListField(child=IntegerField(), required=True)
    baselineBool = BooleanField(required=False)
