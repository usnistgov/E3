from rest_framework.fields import DecimalField, ListField, CharField, IntegerField, DictField
from rest_framework.serializers import Serializer

from API.serializers.fields import SpecialValueDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class AlternativeSummarySerializer(Serializer):
    altID = IntegerField(required=True)
    totalBenefits = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCosts = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsInv = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsNonInv = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    netBenefits = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    netSavings = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SIR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    IRR = DecimalField(max_digits=MAX_DIGITS, decimal_places=3, required=False, allow_null=True)
    AIRR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    DPP = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SPP = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    BCR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    quantSum = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantUnits = DictField(child=CharField())
    MARR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    deltaQuant = DictField(child=SpecialValueDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsPercQuant = DictField(child=SpecialValueDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsDeltaQuant = DictField(child=SpecialValueDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsElasticityQuant = DictField(child=SpecialValueDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)


    def validate(self, data):
        # check that MARR is taken directly from Analysis object.

        return data