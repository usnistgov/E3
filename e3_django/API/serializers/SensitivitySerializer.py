from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, ChoiceField, ListField, BooleanField, CharField

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class SensitivitySerializer(Serializer):
    globalVarBool = BooleanField(required=False)
    altID = ListField(child=IntegerField(), required=True, allow_null=True)
    bcnID = IntegerField(min_value=0, required=True, allow_null=True)
    varName = ChoiceField([
        "discountRate", "initialOcc", "bcnLife", "recurValue", "recurEndDate", "valuePerQ", "quant", "quantValue"],
        required=True
    )
    diffType = ChoiceField(["Percent", "Gross"], 
        required=True
    )
    diffValue = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, 
        required=True
    )

    def validate(self, data):
        if data['globalVarBool'] is False:
            if data['altID'] is None:
                raise ValidationError("altID cannot be null when globalVarBool is False")
                
            if data['bcnID'] is None:
                raise ValidationError("bcnID cannot be null when globalVarBool is False")

        # Check bcnID references an existing BCN object
        # Ensure initialOcc doesn't occur after recurEndDate, other valid ranges for  variable being carried over
        return data
