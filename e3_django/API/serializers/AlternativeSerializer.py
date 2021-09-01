from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField, ListField, BooleanField
from rest_framework.serializers import Serializer


class AlternativeSerializer(Serializer):
    altID = IntegerField(min_value=0, required=True)
    altName = CharField(required=False)
    altBCNList = ListField(child=IntegerField(), required=True)
    baselineBool = BooleanField(required=False)

def validate(self, data):
        # Ensure list of bcnIDs exist, and all bcnIDs reference existing BCN objects.
        for i, x in enumerate(objectList.bcnObject):			
            if x.bcnID != self.altBCNList[i]:
                raise ValidationError("alternativeBCNList does not match the list of bcnIDs of the object")
    	
        # Ensure that only one alternative has baselineBool = True.
        boolCount = 0
        for i, x in enumerate(objectList.bcnObject):
            if x.baselineBool: 
                boolCount += 1
        if boolCount > 1:
            raise ValidationError("only one alternative can have baselineBool = True")

        return data
