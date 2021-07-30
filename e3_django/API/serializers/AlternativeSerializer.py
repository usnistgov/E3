from rest_framework.fields import IntegerField, CharField, ListField, BooleanField
from rest_framework.serializers import Serializer

from API.objects.Alternative import Alternative


class AlternativeSerializer(Serializer):
    altID = IntegerField(min_value=0, required=True)
    altName = CharField(required=False)
    altBCNList = ListField(child=IntegerField(), required=False)
    baselineBool = BooleanField(required=False)
