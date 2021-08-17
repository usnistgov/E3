from rest_framework.serializers import Serializer
from rest_framework.excaptions import ValidationError
from rest_framework.fields import DecimalField, ListField, CharField

from API.variables import MAX_DIGITS, DECIMAL_PLACES


class AlternativeSummarySerializer(Serializer):
    altID = ListField(unique=True, required=True)
    totalBenefits = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCosts = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsInv = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsNonInv = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    netBenefits = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    netSavings = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    SIR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    IRR = DecimalField(max_digits=MAX_DIGITS, decimal_places=3, required=False)
    AIRR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    DPP = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    SPP = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    BCR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    quantSum = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantUnits = ListField(child=CharField())
    MARR = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    deltaQuant = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    nsDeltaQuant = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    nsPercQuant = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    nsElasticityQuant = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))


    def validate(self, data):
        # check that MARR is taken directly from Analysis object.
        
        return data