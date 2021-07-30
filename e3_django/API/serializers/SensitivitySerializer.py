from rest_framework.serializers import Serializer


class SensitivitySerializer(Serializer):
    pass

    # globalVarBool = BooleanField(required=True)
    # altID = IntegerField(required=False)  # TODO represent required property
    # bcnID = IntegerField(required=False)  # TODO represent required property
    # varName = ChoiceField([
    #    "initialOcc", "bcnLife", "recurValue", "recurEndDate", "valuePerQ", "quant", 'quantValue'],
    #    required=True
    # )
    # diffType = ChoiceField(["Percent", "Gross"], required=True)
    # diffValue = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
