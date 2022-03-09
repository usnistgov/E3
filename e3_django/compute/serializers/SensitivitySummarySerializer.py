from rest_framework.fields import ListField, IntegerField, DictField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES
from compute.serializers import AlternativeSummarySerializer


class SensitivitySummarySerializer(Serializer):
    """
    Object serializer for sensitivity summary.
    """
    altID = IntegerField(required=True)
    sensID = IntegerField(required=True)
    totalBenefits = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsInv = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsNonInv = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totTagFlows = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    netBenefits = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    netSavings = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SIR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    IRR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=3, required=False, allow_null=True)
    AIRR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    DPP = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SPP = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    BCR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    quantSum = ListField(child=InfinityDecimalField())
    quantUnits = ListField()
    MARR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    deltaQuant = ListField(child=InfinityDecimalField())
    nsDeltaQuant = ListField(child=InfinityDecimalField())
    nsPercQuant = ListField(child=InfinityDecimalField())
    nsElasticityQuant = ListField(child=InfinityDecimalField())

    # output for sensitivity
    output = ListField(child=AlternativeSummarySerializer, required=True)


    def updateMeasure(self, data, measureName, flow):
        # Reset current measure to the input measure
        data[measureName] = flow
        return data